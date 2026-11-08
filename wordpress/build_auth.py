"""Gera o conteúdo das páginas de login, cadastro, conta e senha no visual da marca."""
import json, os

CSS = r"""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
.tfn-auth{--bg:#000;--panel:#0D1115;--panel2:#11161B;--sunk:#0A0C0F;--line:#2A333B;--line2:#1C2228;--ink:#E8EAED;--ink2:#C3CAD1;--muted:#8A949D;--lime:#A8E05F;--lime-soft:rgba(168,224,95,.12);--lime-line:rgba(168,224,95,.45);--red:#FF6370;--ease:cubic-bezier(.2,.7,.2,1);
 min-height:100vh;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:15px;line-height:1.55;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);-webkit-font-smoothing:antialiased}
.tfn-auth *{box-sizing:border-box}
.tfn-auth .mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.tfn-auth .side{position:relative;overflow:hidden;padding:40px max(28px,5vw);display:flex;flex-direction:column;justify-content:space-between;gap:36px;border-right:1px solid var(--line2);background:radial-gradient(120% 80% at 0% 0%,rgba(168,224,95,.08),transparent 55%),var(--panel)}
.tfn-auth .top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.tfn-auth .brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.tfn-auth .brand b{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:13px;letter-spacing:.22em;color:var(--ink)}
.tfn-auth a.back{color:var(--muted);text-decoration:none;transition:color .2s}
.tfn-auth a.back:hover{color:var(--lime)}
.tfn-auth h1{margin:0;font-size:clamp(32px,4.4vw,56px);font-weight:600;line-height:1.02;letter-spacing:-.025em;text-transform:uppercase;color:var(--ink)}
.tfn-auth h1 span{color:var(--lime)}
.tfn-auth .lede{margin:16px 0 0;color:var(--ink2);max-width:46ch;font-size:16px}
.tfn-auth ul.perks{list-style:none;margin:28px 0 0;padding:0;display:grid;gap:10px;max-width:520px}
.tfn-auth ul.perks li{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--line2);background:rgba(10,12,15,.6);border-radius:2px;padding:12px 14px;color:var(--ink2);font-size:14px}
.tfn-auth ul.perks li b{color:var(--ink);font-weight:500}
.tfn-auth ul.perks svg{flex:none;margin-top:2px;color:var(--lime)}
.tfn-auth .status{display:flex;align-items:center;gap:10px}
.tfn-auth .status b{color:var(--lime);font-weight:500;letter-spacing:.04em}
.tfn-auth .dot{width:8px;height:8px;border-radius:50%;background:var(--lime)}
.tfn-auth svg.wave{position:absolute;right:-40px;bottom:90px;width:70%;max-width:520px;opacity:.35;pointer-events:none}
.tfn-auth .main{display:flex;align-items:center;justify-content:center;padding:40px max(20px,4vw)}
.tfn-auth .card{width:100%;max-width:460px;display:grid;gap:18px}
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
@media (max-width:900px){.tfn-auth{grid-template-columns:1fr}.tfn-auth .side{border-right:0;border-bottom:1px solid var(--line2);padding:28px 20px;gap:22px}.tfn-auth ul.perks,.tfn-auth svg.wave,.tfn-auth .side-foot{display:none}.tfn-auth h1{font-size:clamp(28px,8vw,40px)}.tfn-auth .main{padding:32px 20px 48px;align-items:flex-start}}
@media (prefers-reduced-motion:no-preference){
 .tfn-auth .side>*,.tfn-auth .card{animation:tfnA .6s var(--ease) both}
 .tfn-auth .card{animation-delay:.12s}
 .tfn-auth ul.perks li{animation:tfnA .5s var(--ease) both}
 .tfn-auth ul.perks li:nth-child(2){animation-delay:.08s}.tfn-auth ul.perks li:nth-child(3){animation-delay:.16s}
 .tfn-auth .dot{animation:tfnP 2s ease-out infinite}
 .tfn-auth svg.wave path{stroke-dasharray:1200;stroke-dashoffset:1200;animation:tfnD 2.4s .3s var(--ease) forwards}
 @keyframes tfnA{from{transform:translateY(12px)}to{transform:none}}
 @keyframes tfnP{0%{box-shadow:0 0 0 0 rgba(168,224,95,.55)}80%,100%{box-shadow:0 0 0 9px rgba(168,224,95,0)}}
 @keyframes tfnD{to{stroke-dashoffset:0}}
}
</style>"""

LOGO = '<svg width="34" height="34" viewBox="0 0 38 38" aria-hidden="true"><rect x=".5" y=".5" width="37" height="37" rx="2" fill="#0A0C0F" stroke="#2A333B"/><path d="M7 13c5 0 6 14 12 14s7-16 12-16" fill="none" stroke="#A8E05F" stroke-width="2.4" stroke-linecap="round"/><circle cx="19" cy="27" r="2.6" fill="#A8E05F"/></svg>'
CHECK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'
PERKS = [
    ("Straddle B3", "como cada ação reagiu depois de cair ou subir X% num pregão"),
    ("Sinais do último pregão", "filtrados pelas suas regras de acerto, trades e perda máxima"),
    ("Central de Notícias", "morning call, fluxo de notícias e cotações do dia"),
]
SCRIPT = """<script>(function(){fetch('https://fabricionicolauxx-dev.github.io/straddle-b3/data/meta.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(m){if(!m)return;var s=String(m.last),e=document.getElementById('tfn-auth-last');if(e)e.textContent=s.slice(6,8)+'/'+s.slice(4,6)+'/'+s.slice(0,4);var a=document.getElementById('tfn-auth-acoes');if(a)a.textContent=m.acoes;}).catch(function(){});})();</script>"""


def page(h1a, h1b, lede, title, sub, shortcode, alt_html, perks=True):
    perks_html = ""
    if perks:
        perks_html = '<ul class="perks">' + "".join(
            f'<li>{CHECK}<span><b>{t}</b>: {d}</span></li>' for t, d in PERKS) + "</ul>"
    return f"""<div class="tfn-auth">{CSS}
<aside class="side">
  <div class="top">
    <a class="brand" href="/">{LOGO}<b>STRADDLE B3</b></a>
    <a class="back mono" href="/">← Voltar ao site</a>
  </div>
  <div>
    <span class="mono">Área do trader</span>
    <h1 style="margin-top:14px">{h1a}<br><span>{h1b}</span></h1>
    <p class="lede">{lede}</p>
    {perks_html}
  </div>
  <div class="status mono side-foot"><span class="dot" aria-hidden="true"></span>Dados até o pregão de <b id="tfn-auth-last">–</b> · <b id="tfn-auth-acoes">–</b> ações</div>
  <svg class="wave" viewBox="0 0 520 220" aria-hidden="true"><path d="M0 60 C90 60 100 200 200 200 S320 30 400 40 490 130 520 130" fill="none" stroke="#A8E05F" stroke-width="2.5" stroke-linecap="round"/></svg>
</aside>
<main class="main">
  <div class="card">
    <div><span class="mono">{title[0]}</span><h2 style="margin-top:8px">{title[1]}</h2></div>
    <p class="sub">{sub}</p>
    {shortcode}
    {alt_html}
    <p class="legal">Conteúdo informativo e estatístico. Não é recomendação de investimento.</p>
  </div>
</main>
{SCRIPT}
</div>"""


pages = {
    "659": page("Bem-vindo de volta.", "Sua mesa está pronta.",
                "Entre para abrir o Straddle B3, ver os sinais do último pregão e acompanhar a Central de Notícias.",
                ("Entrar", "Acesse sua conta"), "Use o usuário ou e-mail e a senha do seu cadastro.",
                '[ultimatemember form_id="655"]',
                ''),
    "660": page("Crie sua conta", "e acesse grátis.",
                "Cadastro rápido, sem cartão. Você entra na hora e já pode usar todas as ferramentas da área do trader.",
                ("Cadastro gratuito", "Crie sua conta"), "Leva menos de um minuto.",
                '[ultimatemember form_id="654"]',
                ''),
    "664": page("Recupere", "seu acesso.",
                "Informe o e-mail ou usuário do cadastro. Enviamos um link para você criar uma nova senha.",
                ("Senha", "Recuperar senha"), "Confira também a caixa de spam.",
                '[ultimatemember_password]',
                '<p class="alt">Lembrou a senha? <a href="/login/">Entrar</a></p>', perks=False),
    "663": page("Minha", "conta.",
                "Atualize seus dados de cadastro, e-mail e senha.",
                ("Conta", "Seus dados"), "As alterações valem na hora.",
                '[ultimatemember_account]',
                '<p class="alt"><a href="/area-do-trader/">← Voltar para a área do trader</a></p>', perks=False),
}
out = {k: "<!-- wp:html -->\n" + v + "\n<!-- /wp:html -->" for k, v in pages.items()}
json.dump(out, open(os.path.join(os.path.dirname(__file__), "auth-pages.json"), "w", encoding="utf-8"), ensure_ascii=False)
print({k: len(v) for k, v in out.items()})
