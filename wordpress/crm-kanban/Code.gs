/**
 * Ponte entre a planilha "Leads Straddle B3" (aba CRM) e o Kanban privado do site.
 * Publicado como App da Web: Executar como "Eu", acesso "Qualquer pessoa".
 * Toda chamada precisa do TOKEN abaixo (o mesmo que está na página privada do WordPress).
 */
const TOKEN = '__TOKEN__';
const ABA_CRM = 'CRM';
const ABA_FORM = 'Leads página inicial';
const TZ = 'America/Sao_Paulo';
const ETAPAS = ['Novo', 'Contatado', 'Respondeu', 'Chamada marcada', 'Proposta enviada', 'Quase fechando', 'Em pausa', 'Fechou', 'Perdido'];
// Colunas da aba CRM (A..J). J = Lembrete no formato "AAAA-MM-DD HH:MM|Tipo|Nota"
const COLS = ['nome', 'whatsapp', 'origem', 'entrada', 'etapa', 'ultimoContato', 'proximoPasso', 'dataProximo', 'obs', 'lembrete'];
const DATAS = ['entrada', 'ultimoContato', 'dataProximo'];

function resposta_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  if (!e || !e.parameter || e.parameter.token !== TOKEN) return resposta_({ ok: false, erro: 'acesso negado' });
  return resposta_({ ok: true, etapas: ETAPAS, leads: listar_(), agora: new Date().toISOString() });
}

function doPost(e) {
  let body;
  try { body = JSON.parse(e.postData.contents); } catch (err) { return resposta_({ ok: false, erro: 'pedido inválido' }); }
  if (body.token !== TOKEN) return resposta_({ ok: false, erro: 'acesso negado' });
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    if (body.acao === 'atualizar') return resposta_(atualizar_(body.row, body.nome, body.campos || {}));
    if (body.acao === 'adicionar') return resposta_(adicionar_(body.campos || {}));
    return resposta_({ ok: false, erro: 'ação desconhecida' });
  } finally {
    lock.releaseLock();
  }
}

function aba_() { return SpreadsheetApp.getActive().getSheetByName(ABA_CRM); }

function paraIso_(v) {
  if (v instanceof Date) return Utilities.formatDate(v, TZ, 'yyyy-MM-dd');
  const m = String(v || '').match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  return m ? m[3] + '-' + m[2] + '-' + m[1] : String(v || '');
}

function paraCelula_(campo, v) {
  v = v == null ? '' : String(v).trim();
  if (DATAS.indexOf(campo) >= 0) {
    const m = v.match(/^(\d{4})-(\d{2})-(\d{2})$/);
    return m ? new Date(+m[1], +m[2] - 1, +m[3], 12) : '';
  }
  if (campo === 'whatsapp') return v ? "'" + v.replace(/\D/g, '') : '';
  if (campo === 'lembrete') return v ? "'" + v : '';
  return v;
}

function listar_() {
  const sh = aba_();
  const n = sh.getLastRow() - 1;
  if (n < 1) return [];
  const vals = sh.getRange(2, 1, n, COLS.length).getValues();
  const out = [];
  vals.forEach(function (r, i) {
    if (!String(r[0]).trim()) return;
    const lead = { row: i + 2 };
    COLS.forEach(function (c, j) { lead[c] = DATAS.indexOf(c) >= 0 ? paraIso_(r[j]) : String(r[j]); });
    out.push(lead);
  });
  return out;
}

function atualizar_(row, nome, campos) {
  const sh = aba_();
  row = Number(row);
  if (!(row >= 2 && row <= sh.getLastRow())) return { ok: false, erro: 'linha não encontrada' };
  const atual = String(sh.getRange(row, 1).getValue()).trim();
  if (atual !== String(nome || '').trim()) return { ok: false, erro: 'a planilha mudou; recarregue o quadro', conflito: true };
  if (campos.etapa && ETAPAS.indexOf(campos.etapa) < 0) return { ok: false, erro: 'etapa inválida' };
  Object.keys(campos).forEach(function (c) {
    const j = COLS.indexOf(c);
    if (j >= 0) sh.getRange(row, j + 1).setValue(paraCelula_(c, campos[c]));
  });
  return { ok: true, row: row };
}

function adicionar_(campos) {
  if (!String(campos.nome || '').trim()) return { ok: false, erro: 'nome obrigatório' };
  const sh = aba_();
  const linha = COLS.map(function (c) { return paraCelula_(c, campos[c]); });
  if (!linha[4]) linha[4] = 'Novo';
  if (!linha[3]) linha[3] = paraCelula_('entrada', Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd'));
  const row = primeiraLinhaVazia_(sh);
  sh.getRange(row, 1, 1, COLS.length).setValues([linha]);
  return { ok: true, row: row };
}

function primeiraLinhaVazia_(sh) {
  const n = Math.max(sh.getLastRow(), 1);
  const a = sh.getRange(1, 1, n, 1).getValues();
  for (let i = a.length - 1; i >= 0; i--) if (String(a[i][0]).trim()) return i + 2;
  return 2;
}

/**
 * Leads novos do formulário → CRM (etapa "Novo"). Roda sozinho a cada 10 minutos.
 * Só olha linhas do formulário depois da última já processada e pula telefones que já estão no CRM.
 */
function sincronizarFormulario() {
  const props = PropertiesService.getScriptProperties();
  const form = SpreadsheetApp.getActive().getSheetByName(ABA_FORM);
  const ultima = Number(props.getProperty('ULTIMA_LINHA_FORM') || form.getLastRow());
  const fim = form.getLastRow();
  if (fim <= ultima) { props.setProperty('ULTIMA_LINHA_FORM', String(fim)); return; }
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const sh = aba_();
    const tel = function (v) { return String(v || '').replace(/\D/g, '').replace(/^55(?=\d{10,11}$)/, '').slice(-11); };
    const existentes = {};
    sh.getRange(2, 2, Math.max(sh.getLastRow() - 1, 1), 1).getValues().forEach(function (r) { const t = tel(r[0]); if (t) existentes[t] = true; });
    const novos = form.getRange(ultima + 1, 1, fim - ultima, 4).getValues(); // Data, Nome, E-mail, WhatsApp
    novos.forEach(function (r) {
      const nome = String(r[1]).trim(), t = tel(r[3]);
      if (!nome || (t && existentes[t])) return;
      const quando = horaFormulario_(r[0]);
      const hora = isNaN(quando) ? '' : Utilities.formatDate(quando, TZ, "HH'h'mm");
      adicionar_({
        nome: nome, whatsapp: t, origem: 'Google', etapa: 'Novo',
        entrada: isNaN(quando) ? '' : Utilities.formatDate(quando, TZ, 'yyyy-MM-dd'),
        proximoPasso: 'Mandar primeira mensagem',
        obs: 'Formulário' + (hora ? ' às ' + hora : '') + (r[2] ? ' (' + r[2] + ')' : '')
      });
      if (t) existentes[t] = true;
    });
    props.setProperty('ULTIMA_LINHA_FORM', String(fim));
  } finally {
    lock.releaseLock();
  }
}

/** O formulário grava o horário em UTC como se fosse horário local; aqui viramos o instante certo. */
function horaFormulario_(v) {
  let p;
  if (v instanceof Date) {
    const tzPlanilha = SpreadsheetApp.getActive().getSpreadsheetTimeZone();
    p = Utilities.formatDate(v, tzPlanilha, 'yyyy-MM-dd-HH-mm').split('-').map(Number);
  } else {
    const m = String(v || '').match(/(\d{2})\/(\d{2})\/(\d{4})\s+(\d{1,2}):(\d{2})/);
    if (!m) return new Date(NaN);
    p = [+m[3], +m[2], +m[1], +m[4], +m[5]];
  }
  return new Date(Date.UTC(p[0], p[1] - 1, p[2], p[3], p[4]));
}

/** Rodar UMA vez: marca o ponto de partida do formulário e liga a sincronização a cada 10 min. */
function configurar() {
  const form = SpreadsheetApp.getActive().getSheetByName(ABA_FORM);
  PropertiesService.getScriptProperties().setProperty('ULTIMA_LINHA_FORM', String(form.getLastRow()));
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'sincronizarFormulario') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('sincronizarFormulario').timeBased().everyMinutes(10).create();
}
