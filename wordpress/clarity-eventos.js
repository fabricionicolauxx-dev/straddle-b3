/* Clarity: marcações de conversão e campanha (Trader Fabricio Nicolau) */
(function () {
  window.clarity = window.clarity || function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
  var c = window.clarity, done = {};
  function ev(n, up) { if (done[n]) return; done[n] = 1; try { c('event', n); if (up) c('upgrade', n); } catch (e) {} }
  function tag(k, v) { try { if (v) c('set', k, String(v).slice(0, 100)); } catch (e) {} }

  /* Origem da visita (UTM / Google Ads) — guardada na sessão do navegador */
  var p = new URLSearchParams(location.search), keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  var st = {};
  try { st = JSON.parse(sessionStorage.getItem('tfn_origem') || '{}'); } catch (e) {}
  keys.forEach(function (k) { if (p.get(k)) st[k] = p.get(k); });
  if (p.get('gclid') || p.get('gbraid') || p.get('wbraid')) st.google_ads = 'sim';
  try { sessionStorage.setItem('tfn_origem', JSON.stringify(st)); } catch (e) {}
  keys.forEach(function (k) { tag(k, st[k]); });
  tag('google_ads', st.google_ads || 'nao');
  var path = location.pathname.replace(/\/+$/, '') || '/';
  tag('pagina', path);
  if (document.body && document.body.classList.contains('logged-in')) tag('logado', 'sim');

  /* Página de obrigado = lead confirmado do formulário */
  if (/^\/obrigado/.test(path)) ev('lead_formulario_confirmado', true);

  function init() {
    var homeForm = document.querySelector('#tfn-form-slot form, .elementor-form');
    if (homeForm) {
      /* Formulário apareceu na tela */
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es, o) { es.forEach(function (x) { if (x.isIntersecting) { ev('form_visto'); o.disconnect(); } }); }, { threshold: 0.5 }).observe(homeForm);
      }
    }
    /* Começou a preencher */
    document.addEventListener('focusin', function (e) {
      var f = e.target.closest && e.target.closest('form');
      if (!f) return;
      if (f.classList.contains('elementor-form')) ev('form_inicio');
      else if (f.closest('.um-register')) ev('cadastro_inicio');
      else if (f.closest('.um-login')) ev('login_inicio');
    });
    /* Enviou */
    document.addEventListener('submit', function (e) {
      var f = e.target;
      if (f.classList && f.classList.contains('elementor-form')) ev('form_enviado');
      else if (f.closest && f.closest('.um-register')) ev('cadastro_enviado', true);
    }, true);
    if (window.jQuery) jQuery(document).on('submit_success', function () { ev('lead_formulario', true); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();

  /* Cliques: WhatsApp, CTAs, telefone, e-mail, Straddle */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a,button');
    if (!a) return;
    var h = (a.getAttribute('href') || '').toLowerCase(), t = (a.textContent || '').trim().toLowerCase();
    if (/wa\.me|whatsapp\.com|api\.whatsapp/.test(h)) ev('clique_whatsapp', true);
    else if (h.indexOf('tel:') === 0) ev('clique_telefone');
    else if (h.indexOf('mailto:') === 0) ev('clique_email');
    else if (/acoesb3|straddle/.test(h)) ev('clique_straddle');
    else if (/registro|register|cadastr/.test(h)) ev('clique_cadastro');
    else if (/#tfn-form|#form|#inscri/.test(h) || /inscrev|quero|garant|vaga/.test(t)) ev('clique_cta');
  }, true);

  /* Leitura: rolou 75% da página */
  window.addEventListener('scroll', function () {
    var d = document.documentElement;
    if ((window.scrollY + window.innerHeight) / d.scrollHeight > 0.75) ev('rolou_75');
  }, { passive: true });
})();
