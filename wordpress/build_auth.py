"""Gera o conteúdo das páginas de login, cadastro, conta e senha no visual da Central de Notícias."""
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
LOGO=open(os.path.join(HERE,"logo_datauri.txt")).read().strip()
AVATAR=open(os.path.join(HERE,"avatar_datauri.txt")).read().strip()
CSS = r"""<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
.tfn-auth{--bg:#000;--panel:#0D1115;--panel2:#11161B;--sunk:#0A0C0F;--line:#2A333B;--line2:#1C2228;--ink:#E8EAED;--ink2:#C3CAD1;--muted:#8A949D;--lime:#A8E05F;--lime-soft:rgba(168,224,95,.12);--lime-line:rgba(168,224,95,.45);--red:#FF6370;--ease:cubic-bezier(.2,.7,.2,1);
 min-height:100vh;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:15px;line-height:1.55;padding-bottom:56px;-webkit-font-smoothing:antialiased}
.tfn-auth *{box-sizing:border-box}
.tfn-auth .mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.tfn-auth .hdr{--panel:#0D1115;--panel2:#11161B;--line:#2A333B;--line2:#1C2228;--ink:#E8EAED;--muted:#8A949D;--lime:#A8E05F;--lime-soft:rgba(168,224,95,.12);background:var(--panel);border-bottom:1px solid var(--line2)}
html[data-tfn-theme=light] .tfn-auth{--bg:#F4F6F7;--panel:#FFFFFF;--panel2:#F0F3F5;--sunk:#F7F9FA;--line:#D3DAE0;--line2:#E3E8EC;--ink:#0D1115;--ink2:#2F3943;--muted:#5D6772;--lime:#4F8A12;--lime-soft:rgba(79,138,18,.10);--lime-line:rgba(79,138,18,.40);--red:#D13447}
html[data-tfn-theme=light] .tfn-auth .mc{background:linear-gradient(180deg,#FFFFFF 0%,#F7F9FA 100%)}
html[data-tfn-theme=light] .tfn-auth .mc-r{background:rgba(240,243,245,.6)}
html[data-tfn-theme=light] .tfn-auth svg.chart path.ln{stroke:#4F8A12}
html[data-tfn-theme=light] .tfn-auth .um .um-button:not(.um-alt){color:#FFFFFF!important}
html[data-tfn-theme=light] .tfn-auth .um .um-field-error,html[data-tfn-theme=light] .tfn-auth .um .um-notice.err{color:#FFFFFF!important}
html[data-tfn-theme=light] .tfn-auth .um input:-webkit-autofill{-webkit-box-shadow:0 0 0 40px #F7F9FA inset!important}
.tfn-auth,.tfn-auth .mc,.tfn-auth .mc-r,.tfn-auth .um input{transition:background-color .3s,border-color .3s,color .3s}
.tfn-auth .tt{width:42px;height:42px;padding:0;display:inline-flex;align-items:center;justify-content:center;background:transparent;cursor:pointer;color:var(--ink)}
.tfn-auth .tt .i-sun{display:none}
html[data-tfn-theme=light] .tfn-auth .tt .i-sun{display:block}
html[data-tfn-theme=light] .tfn-auth .tt .i-moon{display:none}
.tfn-auth .hdr-in{max-width:1200px;margin:0 auto;padding:20px max(20px,3vw);display:flex;align-items:center;gap:18px 22px;flex-wrap:wrap}
.tfn-auth .logo{display:flex;align-items:center}
.tfn-auth .logo img{height:48px;width:auto;display:block}
.tfn-auth .vsep{width:1px;height:26px;background:var(--line)}
.tfn-auth .hdr-label{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.tfn-auth nav.nav{display:flex;gap:10px;flex-wrap:wrap;margin-left:18px}
.tfn-auth .nb{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);border-radius:2px;padding:11px 18px;text-decoration:none;transition:color .2s,border-color .2s,background-color .2s;white-space:nowrap}
.tfn-auth .nb:hover{color:var(--ink);border-color:#6F7A83}
.tfn-auth .nb.on{color:var(--lime);border-color:var(--lime);background:var(--lime-soft)}
.tfn-auth .nb.home{margin-left:auto;color:var(--ink);background:var(--panel2)}
.tfn-auth .wrapc{max-width:1200px;margin:28px auto 0;padding:0 max(20px,3vw)}
.tfn-auth .mc{border:1px solid var(--line2);border-radius:2px;background:linear-gradient(180deg,#0D1115 0%,#0A0C0F 100%);display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);overflow:hidden}
.tfn-auth .mc-l{padding:40px max(24px,3.4vw);position:relative;display:flex;flex-direction:column;gap:26px;min-width:0}
.tfn-auth .mc-r{padding:40px max(24px,3.4vw);border-left:1px solid var(--line2);background:rgba(13,17,21,.55);display:flex;align-items:center;justify-content:center;min-width:0}
.tfn-auth .who{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.tfn-auth .who-l{display:flex;align-items:center;gap:14px}
.tfn-auth .who img{width:54px;height:54px;border-radius:50%;object-fit:cover;border:1px solid var(--line)}
.tfn-auth .who b{display:block;font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:14px;letter-spacing:.22em;color:var(--ink);text-transform:uppercase}
.tfn-auth .who span.s{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;color:var(--lime);text-transform:uppercase}
.tfn-auth .pill{font-family:"IBM Plex Mono",monospace;font-size:13px;letter-spacing:.08em;color:var(--lime);border:1px solid var(--lime);border-radius:2px;padding:9px 14px}
.tfn-auth h1{margin:0;font-size:clamp(30px,3.6vw,46px);font-weight:600;line-height:1.06;letter-spacing:-.02em;text-transform:uppercase;color:var(--ink)}
.tfn-auth h1 span{color:var(--lime);display:block;margin-top:6px}
.tfn-auth .lede{margin:0;color:var(--ink2);max-width:52ch;font-size:16px;line-height:1.65}
.tfn-auth ul.perks{list-style:none;margin:0;padding:0;display:grid;gap:8px;max-width:540px}
.tfn-auth ul.perks li{display:flex;gap:12px;align-items:flex-start;border-top:1px solid var(--line2);padding:12px 0 2px;color:var(--ink2);font-size:14px}
.tfn-auth ul.perks li b{color:var(--ink);font-weight:500}
.tfn-auth ul.perks svg{flex:none;margin-top:3px;color:var(--lime)}
.tfn-auth .status{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.tfn-auth .status b{color:var(--lime);font-weight:500;letter-spacing:.04em}
.tfn-auth .dot{width:8px;height:8px;border-radius:50%;background:var(--lime)}
.tfn-auth svg.chart{width:100%;height:auto;display:block;margin-top:auto}
.tfn-auth .card{width:100%;max-width:440px;display:grid;gap:18px}
.tfn-auth .card h2{margin:0;font-size:24px;font-weight:600;letter-spacing:-.01em;color:var(--ink)}
.tfn-auth .card .sub{margin:-10px 0 0;color:var(--muted);font-size:14px}
.tfn-auth .alt{font-size:14px;color:var(--muted);text-align:center;margin:0}
.tfn-auth .alt a{color:var(--lime);text-decoration:none;border-bottom:1px solid var(--lime-line)}
.tfn-auth .legal{font-size:12px;color:var(--muted);margin:0;text-align:center}
/* Ultimate Member */
.tfn-auth .um{max-width:100%!important;width:100%!important;margin:0!important;padding:0!important;opacity:1!important}
.tfn-auth .um-form{background:transparent!important}
.tfn-auth .um .um-row{margin:0!important}
.tfn-auth .um .um-field{padding:0 0 16px!important}
.tfn-auth .um .um-field-label{margin-bottom:8px!important;border:0!important}
.tfn-auth .um .um-field-label label,.tfn-auth .um .um-field-label{font-family:"IBM Plex Mono",monospace!important;font-size:11px!important;font-weight:400!important;letter-spacing:.14em!important;text-transform:uppercase!important;color:var(--muted)!important;line-height:1.4!important}
.tfn-auth .um .um-field-label .um-field-label-icon,.tfn-auth .um .um-field-label-icon i{color:var(--lime)!important;font-size:13px!important}
.tfn-auth .um .um-req{color:var(--lime)!important}
.tfn-auth .um input[type=text],.tfn-auth .um input[type=password],.tfn-auth .um input[type=email],.tfn-auth .um input[type=tel],.tfn-auth .um input[type=number],.tfn-auth .um input[type=url],.tfn-auth .um textarea,.tfn-auth .um select{background:var(--sunk)!important;border:1px solid var(--line)!important;border-radius:2px!important;color:var(--ink)!important;font-family:"IBM Plex Sans",sans-serif!important;font-size:15px!important;height:48px!important;padding:0 14px!important;box-shadow:none!important;transition:border-color .2s,box-shadow .2s!important}
.tfn-auth .um textarea{height:auto!important;padding:12px 14px!important}
.tfn-auth .um input::placeholder{color:#6F7A83!important;font-family:"IBM Plex Sans",sans-serif!important}
.tfn-auth .um,.tfn-auth .um *{font-family:"IBM Plex Sans",system-ui,sans-serif}
.tfn-auth .um input:focus,.tfn-auth .um textarea:focus,.tfn-auth .um select:focus{border-color:var(--lime)!important;box-shadow:0 0 0 3px rgba(168,224,95,.15)!important;outline:none!important}
.tfn-auth .um input:-webkit-autofill{-webkit-box-shadow:0 0 0 40px var(--sunk) inset!important;-webkit-text-fill-color:var(--ink)!important}
.tfn-auth .um .um-col-alt{margin-top:6px!important;display:grid!important;grid-template-columns:1fr 1fr;gap:10px}
.tfn-auth .um .um-col-alt .um-left,.tfn-auth .um .um-col-alt .um-right,.tfn-auth .um .um-col-alt .um-center{float:none!important;width:auto!important;padding:0!important}
.tfn-auth .um .um-col-alt .um-center{grid-column:1/-1}
.tfn-auth .um .um-button,.tfn-auth .um input[type=submit].um-button{width:100%!important;height:50px!important;background:var(--lime)!important;color:#0A0C0F!important;border:1px solid var(--lime)!important;border-radius:2px!important;font-family:"IBM Plex Mono",monospace!important;font-size:12px!important;font-weight:500!important;letter-spacing:.16em!important;text-transform:uppercase!important;box-shadow:none!important;transition:transform .15s,filter .2s,background-color .2s!important;display:flex!important;align-items:center;justify-content:center;line-height:1!important;padding:0 12px!important}
.tfn-auth .um .um-button:hover{filter:brightness(1.08);transform:translateY(-1px)}
.tfn-auth .um .um-button.um-alt,.tfn-auth .um a.um-button.um-alt{background:transparent!important;color:var(--ink2)!important;border:1px solid var(--line)!important}
.tfn-auth .um .um-button.um-alt:hover{border-color:var(--muted)!important;color:var(--ink)!important;filter:none}
.tfn-auth .um a,.tfn-auth .um .um-link-alt{color:var(--lime)!important;text-decoration:none!important}
.tfn-auth .um .um-col-alt-b{padding-top:14px!important;text-align:center}
.tfn-auth .um .um-field-checkbox-option,.tfn-auth .um .um-field-radio-option,.tfn-auth .um label,.tfn-auth .um p{color:var(--ink2)!important;font-size:14px!important}
.tfn-auth .um .um-field-checkbox-state i,.tfn-auth .um .um-icon-android-checkbox-outline-blank,.tfn-auth .um .um-icon-android-checkbox-outline{color:var(--lime)!important}
.tfn-auth .um .um-field-error{background:var(--red)!important;color:#16080A!important;border-radius:2px!important;font-size:13px!important}
.tfn-auth .um .um-field-error .um-field-arrow{color:var(--red)!important}
.tfn-auth .um .um-notice{border-radius:2px!important;font-size:14px!important}
.tfn-auth .um .um-notice.err{background:var(--red)!important;color:#16080A!important}
.tfn-auth .um .um-notice.success{background:var(--lime)!important;color:#0A0C0F!important}
.tfn-auth .um .um-field-block,.tfn-auth .um .um-gdpr-content,.tfn-auth .um .um-field-area{color:var(--ink2)!important}
.tfn-auth .um .um-gdpr-content{background:var(--sunk)!important;border:1px solid var(--line2)!important;border-radius:2px;padding:12px!important;max-height:180px;overflow:auto;font-size:13px}
.tfn-auth .um .um-toggle-gdpr,.tfn-auth .um .um-gdpr-donot-agree{color:var(--lime)!important}
.tfn-auth .um .um-field-icon i{color:var(--muted)!important}
.tfn-auth .um .um-account-side,.tfn-auth .um .um-account-main{background:transparent!important}
.tfn-auth .um .um-account-side li a{background:var(--panel)!important;color:var(--ink2)!important;border:1px solid var(--line2)!important;border-radius:2px;margin-bottom:6px}
.tfn-auth .um .um-account-side li a.current,.tfn-auth .um .um-account-side li a:hover{color:var(--lime)!important;border-color:var(--lime-line)!important}
.tfn-auth .um .um-account-heading{color:var(--ink)!important;font-family:"IBM Plex Sans",sans-serif!important}
.tfn-auth .um .um-account-meta{display:none!important}
@media (max-width:960px){.tfn-auth .mc{grid-template-columns:1fr}.tfn-auth .mc-r{border-left:0;border-top:1px solid var(--line2)}.tfn-auth ul.perks,.tfn-auth svg.chart{display:none}.tfn-auth .mc-l{gap:18px;padding:28px 20px}.tfn-auth .mc-r{padding:28px 20px 36px}}
@media (max-width:760px){.tfn-auth .hdr-label,.tfn-auth .vsep{display:none}.tfn-auth nav.nav{margin-left:0;order:3;width:100%;overflow-x:auto;flex-wrap:nowrap}.tfn-auth .nb{padding:10px 14px}.tfn-auth .logo img{height:40px}}
@media (prefers-reduced-motion:no-preference){
 .tfn-auth .mc{animation:tfnA .6s var(--ease) both}
 .tfn-auth .mc-l>*{animation:tfnA .6s var(--ease) both}
 .tfn-auth .mc-l>*:nth-child(2){animation-delay:.06s}.tfn-auth .mc-l>*:nth-child(3){animation-delay:.12s}.tfn-auth .mc-l>*:nth-child(4){animation-delay:.18s}
 .tfn-auth .card{animation:tfnA .6s .15s var(--ease) both}
 .tfn-auth .dot{animation:tfnP 2s ease-out infinite}
 .tfn-auth svg.chart path.ln{stroke-dasharray:1400;stroke-dashoffset:1400;animation:tfnD 2.4s .3s var(--ease) forwards}
 @keyframes tfnA{from{transform:translateY(12px)}to{transform:none}}
 @keyframes tfnP{0%{box-shadow:0 0 0 0 rgba(168,224,95,.55)}80%,100%{box-shadow:0 0 0 9px rgba(168,224,95,0)}}
 @keyframes tfnD{to{stroke-dashoffset:0}}
}
</style>"""
CHECK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'
CHART = '<svg class="chart" viewBox="0 0 640 150" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="tfnG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A8E05F" stop-opacity=".18"/><stop offset="1" stop-color="#A8E05F" stop-opacity="0"/></linearGradient></defs><path d="M0 130 L80 118 L160 126 L240 92 L320 100 L400 70 L480 78 L560 34 L640 22 L640 150 L0 150Z" fill="url(#tfnG)"/><path class="ln" d="M0 130 L80 118 L160 126 L240 92 L320 100 L400 70 L480 78 L560 34 L640 22" fill="none" stroke="#A8E05F" stroke-width="2.5" stroke-linejoin="round"/></svg>'
PERKS = [
    ("Straddle B3", "como cada ação reagiu depois de cair ou subir X% num pregão"),
    ("Sinais do último pregão", "filtrados pelas suas regras de acerto, trades e perda máxima"),
    ("Central de Notícias", "morning call, fluxo de notícias e cotações do dia"),
]
SCRIPT = """<script>(function(){var d=new Date(),p=function(n){return(n<10?'0':'')+n},e=document.getElementById('tfn-auth-today');if(e)e.textContent=p(d.getDate())+'/'+p(d.getMonth()+1)+'/'+String(d.getFullYear()).slice(2);fetch('https://fabricionicolauxx-dev.github.io/straddle-b3/data/meta.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(m){if(!m)return;var s=String(m.last),x=document.getElementById('tfn-auth-last');if(x)x.textContent=s.slice(6,8)+'/'+s.slice(4,6)+'/'+s.slice(0,4);var a=document.getElementById('tfn-auth-acoes');if(a)a.textContent=m.acoes;}).catch(function(){});})();</script>"""

def page(active, h1a, h1b, lede, title, sub, shortcode, alt_html, perks=True):
    nav = "".join(f'<a class="nb{" on" if key==active else ""}" href="{href}">{label}</a>' for key, href, label in [
        ("noticias", "/central-de-noticias/", "Notícias"), ("straddle", "/ACOESB3/", "Straddle B3"),
        ("login", "/login/", "Entrar"), ("register", "/register/", "Cadastre-se")])
    perks_html = ('<ul class="perks">' + "".join(f'<li>{CHECK}<span><b>{t}</b>: {d}</span></li>' for t, d in PERKS) + "</ul>") if perks else ""
    return f"""<div class="tfn-auth">{CSS}
<header class="hdr"><div class="hdr-in">
  <a class="logo" href="/"><img src="{LOGO}" alt="Insight Financeiro" width="48" height="48"></a>
  <span class="vsep" aria-hidden="true"></span><span class="hdr-label">Área do trader</span>
  <nav class="nav" aria-label="Seções">{nav}</nav>
  <a class="nb home" href="/">Início</a>
  <button type="button" class="nb tt" onclick="window.tfnToggleTheme&&window.tfnToggleTheme()" aria-label="Alternar entre tema claro e escuro" title="Tema claro / escuro"><svg class="i-moon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg><svg class="i-sun" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
</div></header>
<div class="wrapc"><section class="mc">
  <div class="mc-l">
    <div class="who"><div class="who-l"><img src="{AVATAR}" alt="Fabrício Nicolau"><div><b>Área do trader</b><span class="s">Fabrício Nicolau</span></div></div><span class="pill" id="tfn-auth-today">–</span></div>
    <h1>{h1a}<span>{h1b}</span></h1>
    <p class="lede">{lede}</p>
    {perks_html}
    <div class="status mono"><span class="dot" aria-hidden="true"></span>Dados até o pregão de <b id="tfn-auth-last">–</b> · <b id="tfn-auth-acoes">–</b> ações monitoradas</div>
    {CHART if perks else ""}
  </div>
  <div class="mc-r"><div class="card">
    <div><span class="mono">{title[0]}</span><h2 style="margin-top:8px">{title[1]}</h2></div>
    <p class="sub">{sub}</p>
    {shortcode}
    {alt_html}
    <p class="legal">Conteúdo informativo e estatístico. Não é recomendação de investimento.</p>
  </div></div>
</section></div>
{SCRIPT}
</div>"""

pages = {
    "659": page("login", "Bem-vindo de volta.", "Sua mesa está pronta.",
                "Entre para abrir o Straddle B3, ver os sinais do último pregão e acompanhar a Central de Notícias.",
                ("Entrar", "Acesse sua conta"), "Use o usuário ou e-mail e a senha do seu cadastro.",
                '[ultimatemember form_id="655"]', ''),
    "660": page("register", "Crie sua conta", "e acesse grátis.",
                "Cadastro rápido, sem cartão. Você entra na hora e já pode usar todas as ferramentas da área do trader.",
                ("Cadastro gratuito", "Crie sua conta"), "Leva menos de um minuto.",
                '[ultimatemember form_id="654"]', ''),
    "664": page("login", "Recupere", "seu acesso.",
                "Informe o e-mail ou usuário do cadastro. Enviamos um link para você criar uma nova senha.",
                ("Senha", "Recuperar senha"), "Confira também a caixa de spam.",
                '[ultimatemember_password]', '<p class="alt">Lembrou a senha? <a href="/login/">Entrar</a></p>', perks=False),
    "663": page("", "Minha", "conta.",
                "Atualize seus dados de cadastro, e-mail e senha.",
                ("Conta", "Seus dados"), "As alterações valem na hora.",
                '[ultimatemember_account]', '<p class="alt"><a href="/area-do-trader/">← Voltar para a área do trader</a></p>', perks=False),
}
out = {k: "<!-- wp:html -->\n" + v + "\n<!-- /wp:html -->" for k, v in pages.items()}
json.dump(out, open(os.path.join(HERE, "auth-pages.json"), "w", encoding="utf-8"), ensure_ascii=False)
print({k: len(v) for k, v in out.items()})
