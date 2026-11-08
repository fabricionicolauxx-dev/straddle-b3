"""Monta a página "Quem sou" reaproveitando o cabeçalho, o rodapé e os estilos da página inicial."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.join(HERE, "..", "home")
top = open(os.path.join(HOME, "top.html"), encoding="utf-8").read()
bottom = open(os.path.join(HOME, "bottom.html"), encoding="utf-8").read()

top_head = top[: top.index("</style>") + len("</style>")]
header = top[top.index('  <header class="hdr"'): top.index("</header>") + len("</header>")]
header = header.replace('<a class="on" href="/">Início</a>', '<a href="/">Início</a>')
header = header.replace('<a href="/quem-e-trader-fabricio-nicolau/">Quem sou</a>', '<a class="on" href="/quem-e-trader-fabricio-nicolau/">Quem sou</a>')
header = header.replace('<a class="opt" href="#escritorio">Escritório</a>', '<a class="opt" href="/#escritorio">Escritório</a>')
header = header.replace('href="#inscricao"', 'href="/cadastro-aluno/"')
tape = top[top.index('  <div class="tape">'): top.index("  <section class=\"hero\">")]
bottom_style = bottom[: bottom.index("</style>") + len("</style>")]
footer = bottom[bottom.index("  <footer>"): bottom.index("  </footer>") + len("  </footer>")]
script = bottom[bottom.index("<script>"): bottom.rindex("</script>") + len("</script>")]

ICON = {
    "fluxo": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h10M4 12h16M4 17h7"/><circle cx="17" cy="7" r="2"/><circle cx="14" cy="17" r="2"/></svg>',
    "smc": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V10l7-5 7 5v11"/><path d="M9 21v-6h6v6"/></svg>',
    "pa": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/></svg>',
    "b3": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/></svg>',
    "cripto": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 8h4a2 2 0 0 1 0 4h-4m0 0h4.5a2 2 0 0 1 0 4H9.5V8m1.5-2v2m0 8v2m2-12v2m0 8v2"/></svg>',
    "inter": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
    "online": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4"/></svg>',
    "live": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2"/><path d="M16.2 7.8a6 6 0 0 1 0 8.4M7.8 16.2a6 6 0 0 1 0-8.4M19 5a10 10 0 0 1 0 14M5 19A10 10 0 0 1 5 5"/></svg>',
}

css = r"""
<style>
.tfq .qhero{position:relative;overflow:hidden;border-bottom:1px solid var(--line2);background:radial-gradient(70% 90% at 100% 0%,rgba(168,224,95,.07),transparent 60%),#000}
.tfq .qhero-in{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:56px;align-items:center;padding-top:72px;padding-bottom:80px}
.tfq .pill{display:inline-flex;font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--lime);border:1px solid var(--lime);background:var(--lime-soft);border-radius:2px;padding:8px 14px}
.tfq h1{margin:22px 0 0;font-size:clamp(34px,4.6vw,62px);line-height:1.03;font-weight:600;letter-spacing:-.025em;text-transform:uppercase;color:var(--ink)}
.tfq h1 span{display:block;color:var(--lime)}
.tfq .lede{margin:22px 0 0;max-width:56ch;font-size:18px;line-height:1.65;color:var(--ink2)}
.tfq .facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.tfq .fact{border:1px solid var(--line);background:var(--panel);border-radius:2px;padding:12px 16px;display:grid;gap:2px;min-width:150px}
.tfq .fact b{font-family:"IBM Plex Mono",monospace;font-size:22px;font-weight:500;color:var(--ink)}
.tfq .fact b em{font-style:normal;color:var(--lime)}
.tfq .fact span{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.tfq .photo{position:relative;max-width:520px;justify-self:end;width:100%}
.tfq .photo img{display:block;width:100%;height:auto;aspect-ratio:700/657;object-fit:cover;border:1px solid var(--line);border-radius:2px;filter:saturate(.9)}
.tfq .photo::before{content:"";position:absolute;inset:14px -14px -14px 14px;border:1px solid var(--lime-line);border-radius:2px;z-index:-1}
.tfq .photo .cap{position:absolute;left:-1px;bottom:-1px;background:#000;border:1px solid var(--line);border-left:2px solid var(--lime);padding:12px 16px;display:grid;gap:2px}
.tfq .photo .cap b{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:var(--ink)}
.tfq .photo .cap span{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--lime)}
.tfq .story{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px}
.tfq .story p{margin:0 0 16px;color:var(--ink2);font-size:17px;line-height:1.7;max-width:58ch}
.tfq .timeline{list-style:none;margin:0;padding:0;position:relative}
.tfq .timeline::before{content:"";position:absolute;left:7px;top:8px;bottom:8px;width:1px;background:var(--line)}
.tfq .timeline li{position:relative;padding:0 0 28px 36px}
.tfq .timeline li:last-child{padding-bottom:0}
.tfq .timeline li::before{content:"";position:absolute;left:0;top:6px;width:15px;height:15px;border-radius:50%;background:#000;border:2px solid var(--line)}
.tfq .timeline li.now::before{border-color:var(--lime);background:var(--lime)}
.tfq .timeline .when{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--lime)}
.tfq .timeline h3{margin:4px 0 4px;font-size:19px;font-weight:600;color:var(--ink)}
.tfq .timeline p{margin:0;color:var(--muted);font-size:15px}
.tfq .card{background:var(--panel);border:1px solid var(--line2);border-radius:2px;padding:26px;display:grid;gap:12px;align-content:start;transition:border-color .25s,transform .25s var(--ease),background-color .25s}
.tfq .card:hover{border-color:var(--lime-line);transform:translateY(-3px);background:var(--hover)}
.tfq .card h3{margin:0;font-size:21px;font-weight:600;text-transform:uppercase;letter-spacing:-.01em;color:var(--ink)}
.tfq .card p{margin:0;color:var(--muted);font-size:15.5px}
.tfq .markets{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.tfq .market{display:flex;align-items:center;gap:16px;border:1px solid var(--line2);background:var(--panel);border-radius:2px;padding:22px}
.tfq .market h3{margin:0;font-size:18px;font-weight:600;text-transform:uppercase;color:var(--ink)}
.tfq .grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media (max-width:980px){.tfq .qhero-in,.tfq .story{grid-template-columns:1fr;gap:40px}.tfq .photo{justify-self:start;max-width:440px}.tfq .markets,.tfq .grid2{grid-template-columns:1fr}}
@media (max-width:520px){.tfq .lede{font-size:16.5px}.tfq .fact{min-width:0;flex:1 1 40%}.tfq .photo::before{inset:10px -10px -10px 10px}}
@media (prefers-reduced-motion:no-preference){.tfq .qhero-in>*{animation:tfhUp .7s var(--ease) both}.tfq .qhero-in>*:nth-child(2){animation-delay:.12s}}
</style>"""

content = f"""
<div class="tfh">
{header}
{tape}
</div>
<div class="tfh-bottom tfq">
  <section class="qhero">
    <div class="tfh-wrap qhero-in">
      <div>
        <span class="pill">Quem sou</span>
        <h1>Há 10 anos lendo o mercado na prática.<span>Hoje ensino a operar com mais segurança.</span></h1>
        <p class="lede">Especialista em tape reading, formado em Gestão Financeira e criador do Método Híbrido de leitura de fluxo.</p>
        <div class="facts">
          <div class="fact"><b>10 <em>anos</em></b><span>operando</span></div>
          <div class="fact"><b>7 <em>anos</em></b><span>ensinando</span></div>
          <div class="fact"><b><em>+</em>500</b><span>traders formados</span></div>
        </div>
      </div>
      <figure class="photo" style="margin:0">
        <img src="{{{{FOTO}}}}" alt="Fabricio Nicolau, especialista em tape reading" width="700" height="657">
        <figcaption class="cap"><b>Fabricio Nicolau</b><span>Especialista em tape reading</span></figcaption>
      </figure>
    </div>
  </section>

  <section class="sec">
    <div class="tfh-wrap story">
      <div class="rv">
        <span class="mono">A trajetória</span>
        <h2>Aprendeu operando, <span>sem atalhos</span></h2>
        <p style="margin-top:22px">Há 10 anos, Fabricio Nicolau começou a operar gráficos sem cursos de referência disponíveis. O aprendizado veio da prática direta com o mercado: testando, errando e ajustando estratégias no dia a dia.</p>
        <p>Essa base foi somada a uma formação em Gestão Financeira, unindo a vivência de quem operou na raça com o embasamento técnico necessário para entender o mercado de forma estruturada.</p>
        <p>Há 7 anos, essa experiência começou a ser compartilhada: Fabricio passou a ensinar outras pessoas a operar com mais segurança, traduzindo anos de prática em um método claro e replicável.</p>
      </div>
      <ol class="timeline rv">
        <li><span class="when">Há 10 anos</span><h3>Primeiras operações</h3><p>Aprendizado direto com o mercado, sem cursos de referência.</p></li>
        <li><span class="when">Formação</span><h3>Gestão Financeira</h3><p>Base técnica para estruturar a leitura de mercado.</p></li>
        <li><span class="when">Há 7 anos</span><h3>Começa a ensinar</h3><p>A prática vira um método claro e replicável.</p></li>
        <li class="now"><span class="when">Hoje</span><h3>+500 traders formados</h3><p>Cursos online e ao vivo, do escritório no Batel, em Curitiba.</p></li>
      </ol>
    </div>
  </section>

  <section class="sec">
    <div class="tfh-wrap">
      <div class="head rv"><div><span class="mono">O método</span><h2>Método híbrido: <span>fluxo, SMC e price action</span></h2></div><p>Três leituras que se completam para entender quem está comprando, quem está vendendo e para onde o preço tende a ir.</p></div>
      <div class="grid3">
        <div class="card rv"><span class="ico">{ICON['fluxo']}</span><h3>Leitura de fluxo</h3><p>Análise do comportamento de compradores e vendedores em tempo real, direto no livro de ofertas.</p></div>
        <div class="card rv"><span class="ico">{ICON['smc']}</span><h3>Smart Money (SMC)</h3><p>Identificação dos movimentos do "dinheiro inteligente" para entender a estrutura real do mercado.</p></div>
        <div class="card rv"><span class="ico">{ICON['pa']}</span><h3>Price action</h3><p>Leitura do preço puro no gráfico, sem depender de excesso de indicadores.</p></div>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="tfh-wrap">
      <div class="head rv"><div><span class="mono">Onde aplicar</span><h2>Um método, <span>três mercados</span></h2></div></div>
      <div class="markets">
        <div class="market rv"><span class="ico">{ICON['b3']}</span><h3>Bolsa brasileira</h3></div>
        <div class="market rv"><span class="ico">{ICON['cripto']}</span><h3>Mercado cripto</h3></div>
        <div class="market rv"><span class="ico">{ICON['inter']}</span><h3>Mercado internacional</h3></div>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="tfh-wrap">
      <div class="head rv"><div><span class="mono">Como são as aulas</span><h2>Cursos online <span>e ao vivo</span></h2></div></div>
      <div class="grid2">
        <div class="card rv"><span class="ico">{ICON['online']}</span><h3>No seu ritmo, de onde estiver</h3><p>Conteúdo acessível para quem quer aprender a operar sem depender de estar em Curitiba.</p></div>
        <div class="card rv"><span class="ico">{ICON['live']}</span><h3>Contato direto com o Fabricio</h3><p>Aulas ao vivo para tirar dúvidas em tempo real e acompanhar a leitura do mercado junto com o professor.</p></div>
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="tfh-wrap cta-in rv">
      <div><span class="mono">Próximo passo</span><h2>Pronto para aprender a operar <span>com segurança?</span></h2><p style="margin:14px 0 0;color:var(--ink2)">Junte-se aos mais de 500 traders que já passaram pelo método.</p></div>
      <a class="btn pri pulse" href="/cadastro-aluno/" style="padding:18px 26px;font-size:13px">Quero me inscrever agora <span class="arr" aria-hidden="true">→</span></a>
    </div>
  </section>

{footer}
</div>
"""
out = top_head + "\n" + bottom_style + "\n" + css + "\n" + content + "\n" + script
out = out.replace(".tfh-bottom .sec{padding:88px 0;", ".tfh-bottom .sec{padding:88px 0;")
open(os.path.join(HERE, "page.html"), "w", encoding="utf-8").write(out)
print(len(out))
