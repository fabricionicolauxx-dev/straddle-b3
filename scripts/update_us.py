#!/usr/bin/env python3
"""Baixa o histórico diário das ações do S&P 500 + Nasdaq 100 e gera site/data/us.json.

Uso:
    python scripts/update_us.py --out site/data/us.json --start 2024-01-01

- Lista de ações: composição atual na Wikipedia (S&P 500 e Nasdaq-100).
  Se a Wikipedia não responder, usa scripts/us_tickers.txt.
- Cotações: Yahoo Finance (biblioteca yfinance). Preços ajustados por
  desdobramento, sem ajuste de dividendos (mesma ideia da B3).
- Se o download falhar, mantém o arquivo publicado anteriormente no site,
  para a aba EUA não sumir.

Formato igual ao quotes.json da B3: preços em centavos, volume financeiro em dólares.
"""
import argparse
import datetime as dt
import io
import json
import os
import sys
import time
import urllib.request
from zoneinfo import ZoneInfo

UA = "Mozilla/5.0 (X11; Linux x86_64) StraddleB3/1.0 (+https://fabricionicolauxx-dev.github.io/straddle-b3/)"
PREV_URL = "https://fabricionicolauxx-dev.github.io/straddle-b3/data/us.json"
HERE = os.path.dirname(os.path.abspath(__file__))


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def wiki_tickers():
    import pandas as pd
    out = set()
    for name, url in [("S&P 500", "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"),
                      ("Nasdaq-100", "https://en.wikipedia.org/wiki/Nasdaq-100")]:
        html = get(url).decode("utf-8")
        found = set()
        for t in pd.read_html(io.StringIO(html)):
            cols = [str(c).strip().lower() for c in t.columns]
            for key in ("symbol", "ticker"):
                if key in cols:
                    col = t.columns[cols.index(key)]
                    vals = [str(v).strip().upper() for v in t[col] if isinstance(v, str)]
                    vals = [v for v in vals if 1 <= len(v) <= 6 and v.replace(".", "").isalpha()]
                    if len(vals) > len(found):
                        found = set(vals)
        print(f"  {name}: {len(found)} ações")
        if len(found) < (450 if name == "S&P 500" else 90):
            raise RuntimeError(f"tabela do {name} veio incompleta")
        out |= found
    return sorted(out)


def file_tickers():
    path = os.path.join(HERE, "us_tickers.txt")
    with open(path, encoding="utf-8") as f:
        return [l.strip().upper() for l in f if l.strip() and not l.startswith("#")]


def load_previous(path):
    """Arquivo da execução anterior: primeiro o publicado no site, depois um local."""
    try:
        data = json.loads(get(PREV_URL + "?t=%d" % time.time(), timeout=90))
        print(f"  arquivo anterior do site: {len(data.get('tickers', {}))} ações, último pregão {data.get('last')}")
        return data
    except Exception as e:
        print(f"  sem arquivo anterior no site ({e})")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def download(tickers, start):
    import yfinance as yf
    acc = {}
    ysym = {t: t.replace(".", "-") for t in tickers}
    todo = list(tickers)
    for rnd in range(3):
        if not todo:
            break
        if rnd:
            print(f"  nova tentativa para {len(todo)} ações…")
            time.sleep(20 * rnd)
        missing = []
        for i in range(0, len(todo), 80):
            chunk = todo[i:i + 80]
            try:
                df = yf.download([ysym[t] for t in chunk], start=start, interval="1d", auto_adjust=False,
                                 actions=False, group_by="ticker", threads=True, progress=False, timeout=60)
            except Exception as e:
                print(f"  lote {i // 80 + 1}: erro {e}")
                missing += chunk
                continue
            for t in chunk:
                try:
                    sub = df[ysym[t]] if len(chunk) > 1 or ysym[t] in df.columns.get_level_values(0) else df
                    sub = sub.dropna(subset=["Open", "High", "Low", "Close"])
                except Exception:
                    missing.append(t)
                    continue
                rows = {}
                for idx, r in sub.iterrows():
                    c = float(r["Close"])
                    if not c > 0:
                        continue
                    d = int(idx.strftime("%Y%m%d"))
                    o, h, l = float(r["Open"]), float(r["High"]), float(r["Low"])
                    v = float(r["Volume"]) if r["Volume"] == r["Volume"] else 0.0
                    vol = v * c
                    rows[d] = (round((o or c) * 100), round((h or c) * 100), round((l or c) * 100), round(c * 100), round(vol))
                if len(rows) >= 20:
                    acc[t] = rows
                else:
                    missing.append(t)
            time.sleep(2)
        todo = missing
    if todo:
        print(f"  sem dados para {len(todo)} ações: {', '.join(todo[:40])}{'…' if len(todo) > 40 else ''}")
    return acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="site/data/us.json")
    ap.add_argument("--start", default="2024-01-01")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    print("Lista de ações:")
    try:
        tickers = wiki_tickers()
        src_list = "composição atual (Wikipedia)"
    except Exception as e:
        print(f"  Wikipedia falhou ({e}); usando a lista de reserva")
        tickers = file_tickers()
        src_list = "lista de reserva"
    print(f"  total: {len(tickers)} ações")

    print("Arquivo anterior:")
    prev = load_previous(args.out)

    print("Cotações (Yahoo Finance):")
    acc = {}
    try:
        acc = download(tickers, args.start)
    except Exception as e:
        print(f"  download falhou: {e}")

    if len(acc) < len(tickers) * 0.5:
        if prev and prev.get("tickers"):
            print(f"Só {len(acc)} ações baixadas. Mantendo o arquivo anterior.")
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(prev, f, separators=(",", ":"))
            return
        if not acc:
            print("Nenhum dado baixado e nenhum arquivo anterior. A aba EUA fica sem dados nesta execução.")
            return

    # ações que falharam hoje mas existiam antes continuam com o histórico anterior
    if prev and prev.get("tickers"):
        keep = 0
        for t, a in prev["tickers"].items():
            if t in acc or t not in tickers:
                continue
            acc[t] = {d: (a[1][i], a[2][i], a[3][i], a[4][i], a[5][i]) for i, d in enumerate(a[0])}
            keep += 1
        if keep:
            print(f"  {keep} ações mantidas do arquivo anterior")

    last = max(max(m) for m in acc.values())
    cutoff = int((dt.datetime.strptime(str(last), "%Y%m%d") - dt.timedelta(days=30)).strftime("%Y%m%d"))
    out_t = {}
    for t, m in sorted(acc.items()):
        ds = sorted(m)
        if len(ds) < 20 or ds[-1] < cutoff:
            continue
        rows = [m[d] for d in ds]
        out_t[t] = [ds] + [[r[i] for r in rows] for i in range(5)]

    out = {
        "updated": dt.datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="minutes"),
        "last": last,
        "first": min(v[0][0] for v in out_t.values()),
        "source": f"Yahoo Finance — S&P 500 + Nasdaq 100, {src_list} (ajuste só por desdobramento)",
        "tickers": out_t,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))
    size = os.path.getsize(args.out) / 1e6
    print(f"OK: {len(out_t)} ações, último pregão {last}, arquivo {size:.1f} MB")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # nunca derruba a publicação do site da B3
        print(f"Erro inesperado na aba EUA: {e}")
        sys.exit(0)
