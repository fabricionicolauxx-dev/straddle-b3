#!/usr/bin/env python3
"""Baixa as séries históricas oficiais da B3 (COTAHIST) e gera o arquivo de dados do site.

Uso:
    python scripts/update.py --out site/data/quotes.json --start-year 2024

Fontes (públicas e gratuitas, publicadas pela B3):
    Arquivo anual:  COTAHIST_A{AAAA}.ZIP
    Arquivo diário: COTAHIST_D{DDMMAAAA}.ZIP  (usado para completar os últimos pregões)

Só usa a biblioteca padrão do Python.
"""
import argparse
import datetime as dt
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from zoneinfo import ZoneInfo

BASE = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/"
UA = "Mozilla/5.0 (X11; Linux x86_64) StraddleB3/1.0"
TICKER_RE = re.compile(r"^[A-Z0-9]{4}(3|4|5|6|11)$")


def fetch(name, tries=3):
    """Retorna os bytes do arquivo, ou None se a B3 não tiver esse arquivo."""
    url = BASE + name
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            if not data.startswith(b"PK"):
                print(f"  {name}: resposta não é um ZIP, ignorado")
                return None
            print(f"  {name}: {len(data) / 1e6:.1f} MB")
            return data
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                print(f"  {name}: não disponível ({e.code})")
                return None
            print(f"  {name}: erro HTTP {e.code} (tentativa {attempt})")
        except Exception as e:  # rede instável: tenta de novo
            print(f"  {name}: {e} (tentativa {attempt})")
        time.sleep(5 * attempt)
    return None


def parse_cotahist(text, acc):
    """Lê o layout oficial COTAHIST: só ações do mercado à vista, lote padrão."""
    count = 0
    for line in text.splitlines():
        if len(line) < 245 or not line.startswith("01"):
            continue
        if line[10:12] != "02" or line[24:27] != "010":
            continue
        tk = line[12:24].strip()
        if not TICKER_RE.match(tk):
            continue
        fat = int(line[210:217] or 1) or 1
        d = int(line[2:10])
        o = int(line[56:69]) / fat
        h = int(line[69:82]) / fat
        l = int(line[82:95]) / fat
        c = int(line[108:121]) / fat
        v = int(line[170:188]) / 100
        if c <= 0:
            continue
        acc.setdefault(tk, {})[d] = (round(o or c), round(h or c), round(l or c), round(c), round(v))
        count += 1
    return count


def load_zip(data, acc):
    total = 0
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in z.namelist():
            text = z.read(name).decode("latin-1")
            total += parse_cotahist(text, acc)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="site/data/quotes.json")
    ap.add_argument("--start-year", type=int, default=2024)
    ap.add_argument("--daily-days", type=int, default=14, help="quantos dias corridos completar com arquivos diários")
    args = ap.parse_args()

    today = dt.datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    acc = {}

    print("Arquivos anuais:")
    for year in range(args.start_year, today.year + 1):
        data = fetch(f"COTAHIST_A{year}.ZIP")
        if data:
            print(f"    {load_zip(data, acc)} pregões de ações")

    print("Arquivos diários (últimos pregões):")
    for back in range(args.daily_days, -1, -1):
        day = today - dt.timedelta(days=back)
        if day.weekday() >= 5:
            continue
        data = fetch(f"COTAHIST_D{day:%d%m%Y}.ZIP", tries=2)
        if data:
            load_zip(data, acc)

    if not acc:
        print("Nenhum dado baixado. O site continua com a versão anterior.")
        sys.exit(1)

    last = max(max(m) for m in acc.values())
    cutoff = int((dt.datetime.strptime(str(last), "%Y%m%d") - dt.timedelta(days=30)).strftime("%Y%m%d"))
    tickers = {}
    for tk, m in sorted(acc.items()):
        ds = sorted(m)
        if len(ds) < 20 or ds[-1] < cutoff:  # pouco histórico ou parou de negociar
            continue
        rows = [m[d] for d in ds]
        tickers[tk] = [ds] + [[r[i] for r in rows] for i in range(5)]

    out = {
        "updated": dt.datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="minutes"),
        "last": last,
        "first": min(v[0][0] for v in tickers.values()),
        "source": "B3 — Séries históricas COTAHIST (preços sem ajuste de proventos)",
        "tickers": tickers,
    }
    import os
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))
    meta = {"updated": out["updated"], "last": last, "acoes": len(tickers),
            "pregoes": sum(len(v[0]) for v in tickers.values())}
    with open(os.path.join(os.path.dirname(args.out) or ".", "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f)
    size = os.path.getsize(args.out) / 1e6
    print(f"OK: {len(tickers)} ações, último pregão {last}, arquivo {size:.1f} MB")


if __name__ == "__main__":
    main()
