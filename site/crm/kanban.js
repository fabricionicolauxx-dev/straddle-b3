/* CRM Kanban do traderfabricionicolau.com.br/crm/ — a chave fica só na página protegida */
(function(){
const API = (window.CRMK||{}).api;
const TOKEN = (window.CRMK||{}).token;
const STAGES=[["Novo","--s-novo"],["Contatado","--s-contatado"],["Respondeu","--s-respondeu"],["Chamada marcada","--s-chamada"],
 ["Proposta enviada","--s-proposta"],["Quase fechando","--s-quase"],["Fechou","--s-fechou"],["Perdido","--s-perdido"]];
const ORIGENS=["Google","Aluno Wall","YouTube","Discord","Indicação","Outro"];
const TIPOS=["Chamar no WhatsApp","Ligar","Reunião","Follow-up"];
const ICON={
  bell:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 8a6 6 0 1 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>',
  moon:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
  sun:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
};
const root=document.getElementById("crmk");
document.documentElement.style.overflow="hidden";
let leads=[], filtroOrigem=null, busca="", drag=null, salvando=0, ultimaCarga=0, emAlerta=false;
const $=(s,r=root)=>r.querySelector(s);
const el=(t,a={},...k)=>{const e=document.createElement(t);for(const[x,v]of Object.entries(a)){if(x==="class")e.className=v;else if(x==="style")e.style.cssText=v;else if(x==="html")e.innerHTML=v;else if(x.startsWith("on"))e.addEventListener(x.slice(2),v);else if(v!==undefined&&v!==null&&v!==false)e.setAttribute(x,v)}for(const c of k.flat())if(c!=null)e.append(c);return e};
const pad=n=>String(n).padStart(2,"0");
const isoDia=d=>d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate());
const hoje=()=>isoDia(new Date());
const br=iso=>iso&&/^\d{4}-\d{2}-\d{2}$/.test(iso)?iso.split("-").reverse().slice(0,2).join("/"):iso||"";
const fone=n=>{n=(n||"").replace(/\D/g,"");if(n.length===11)return`(${n.slice(0,2)}) ${n.slice(2,7)}-${n.slice(7)}`;if(n.length===10)return`(${n.slice(0,2)}) ${n.slice(2,6)}-${n.slice(6)}`;return n};
const waLink=n=>{n=(n||"").replace(/\D/g,"");return n?"https://wa.me/"+(n.length<=11?"55":"")+n:""};
let tStatus; const status=(t,err)=>{const s=$("#crmk-status");s.textContent=t||"";s.className="note"+(err?" err":"");clearTimeout(tStatus);if(t&&!err)tStatus=setTimeout(()=>s.textContent="",3500)};
const fechado=l=>["Fechou","Perdido"].includes(l.etapa);
const guardar=(k,v)=>{try{localStorage.setItem(k,v)}catch(_){}};
const ler=k=>{try{return localStorage.getItem(k)}catch(_){return null}};

/* ---------- tema ---------- */
function aplicarTema(t){root.dataset.theme=t;const b=$("#crmk-tema");b.innerHTML=(t==="dark"?ICON.sun:ICON.moon)+"<span>"+(t==="dark"?"Tema claro":"Tema escuro")+"</span>";guardar("crmk-tema",t)}
aplicarTema(ler("crmk-tema")==="dark"?"dark":"light");
$("#crmk-tema").addEventListener("click",()=>aplicarTema(root.dataset.theme==="dark"?"light":"dark"));

/* ---------- lembretes: "AAAA-MM-DD HH:MM|Tipo|Nota" ---------- */
function lemb(l){const s=String(l.lembrete||"").trim();if(!s)return null;const p=s.split("|");const m=(p[0]||"").match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})/);if(!m)return null;
  return{quando:new Date(+m[1],+m[2]-1,+m[3],+m[4],+m[5]),dia:m[1]+"-"+m[2]+"-"+m[3],hora:m[4]+":"+m[5],tipo:p[1]||"Follow-up",nota:p.slice(2).join("|"),raw:s}}
const textoLemb=(dia,hora,tipo,nota)=>dia+" "+hora+"|"+tipo.replace(/\|/g,"/")+(nota?"|"+nota.replace(/\|/g,"/"):"");
function quandoCurto(r){const h=hoje(),am=isoDia(new Date(Date.now()+864e5));return(r.dia===h?"hoje":r.dia===am?"amanhã":br(r.dia))+" "+r.hora}
const vencido=r=>r&&r.quando.getTime()<=Date.now();

/* ---------- dados ---------- */
async function api(body){
  const r=await fetch(API,{method:"POST",body:JSON.stringify(Object.assign({token:TOKEN},body)),headers:{"Content-Type":"text/plain;charset=utf-8"}});
  const j=await r.json(); if(!j.ok)throw new Error(j.erro||"erro"); return j;
}
async function carregar(silencioso){
  if(drag&&drag.active||salvando||($("#crmk-drawer").firstChild||$("#crmk-pop").firstChild)&&silencioso)return;
  try{
    const r=await fetch(API+"?token="+encodeURIComponent(TOKEN)+"&t="+Date.now()); const j=await r.json();
    if(!j.ok)throw new Error(j.erro);
    leads=j.leads; ultimaCarga=Date.now(); render(); checarLembretes();
    if(!silencioso)status("Atualizado agora"); else if($("#crmk-status").textContent.indexOf("Carregando")===0)status("");
  }catch(e){status("Não consegui ler a planilha. Confira a internet e clique em Atualizar.",true)}
}
async function salvar(l,campos,desfazer,msg){
  salvando++; const c=root.querySelector(`.card[data-row="${l.row}"]`); if(c)c.classList.add("saving");
  try{await api({acao:"atualizar",row:l.row,nome:l.nome,campos}); status("Salvo na planilha: "+msg); return true}
  catch(e){desfazer&&desfazer(); status("Não salvou: "+e.message+". Clique em Atualizar e tente de novo.",true); return false}
  finally{salvando--; render()}
}

/* ---------- quadro ---------- */
function visiveis(){const q=busca.toLowerCase();return leads.filter(l=>(!filtroOrigem||l.origem===filtroOrigem)&&(!q||[l.nome,l.whatsapp,l.obs,l.proximoPasso,l.lembrete].join(" ").toLowerCase().includes(q)))}
function renderStats(){
  const h=hoje(), ativos=leads.filter(l=>!fechado(l));
  const atras=ativos.filter(l=>l.dataProximo&&l.dataProximo<h).length, hj=ativos.filter(l=>l.dataProximo===h).length;
  const prop=leads.filter(l=>["Proposta enviada","Quase fechando"].includes(l.etapa)).length, fech=leads.filter(l=>l.etapa==="Fechou").length;
  const lembHoje=leads.map(lemb).filter(r=>r&&r.dia<=h).length;
  const s=(v,t,c)=>el("div",{class:"stat"+(c?" "+c:"")},el("b",{},String(v)),el("span",{},t));
  $("#crmk-stats").replaceChildren(s(ativos.length,"Ativos"),s(hj,"Follow-up hoje"),s(atras,"Atrasados",atras>0?"alert":""),s(lembHoje,"Lembretes hoje",lembHoje>0?"bell":""),s(prop,"Em proposta"),s(fech,"Fechados"));
  const total=leads.filter(lemb).length; const b=$("#crmk-lembretes");
  b.innerHTML=ICON.bell+"<span>Lembretes"+(total?" ("+total+")":"")+"</span>"; b.className="btn"+(leads.some(l=>vencido(lemb(l)))?" bellbtn":"");
}
function renderOrigens(){
  const usadas=[...new Set(leads.map(l=>l.origem).filter(Boolean))];
  $("#crmk-origens").replaceChildren(...[null,...usadas].map(o=>el("button",{class:"chip",type:"button","aria-pressed":String(filtroOrigem===o),onclick:()=>{filtroOrigem=o;render()}},o||"Todas")));
}
function card(l){
  const c=`var(${(STAGES.find(s=>s[0]===l.etapa)||STAGES[0])[1]})`, h=hoje(), r=lemb(l), agora=vencido(r);
  const due=l.dataProximo?el("span",{class:"due"+(l.dataProximo<h&&!fechado(l)?" late":l.dataProximo===h?" today":"")},br(l.dataProximo)):null;
  const sino=el("button",{class:"bellchip"+(r?" on":"")+(agora?" now":""),type:"button","aria-label":r?"Lembrete: "+r.tipo+" "+quandoCurto(r):"Criar lembrete",title:r?r.tipo+(r.nota?" · "+r.nota:""):"Criar lembrete",html:ICON.bell+(r?"<span>"+quandoCurto(r)+"</span>":"")});
  sino.addEventListener("pointerdown",ev=>ev.stopPropagation());
  sino.addEventListener("click",ev=>{ev.stopPropagation();abrirLembrete(l)});
  const e=el("div",{class:"card"+(agora?" ring":""),tabindex:"0",style:`--c:${c}`,"data-row":l.row,role:"button","aria-label":l.nome},
    el("div",{class:"row1"},el("div",{class:"nm"},l.nome),l.origem?el("span",{class:"tag"},l.origem):null),
    l.proximoPasso?el("div",{class:"np"},l.proximoPasso):null,
    el("div",{class:"meta"},due,l.whatsapp?el("span",{},fone(l.whatsapp)):null,sino));
  e.addEventListener("keydown",ev=>{if(ev.key==="Enter"&&ev.target===e)abrir(l)});
  e.addEventListener("pointerdown",ev=>{if(ev.button!==0)return;const st={x:ev.clientX,y:ev.clientY,el:e,lead:l,id:ev.pointerId,active:false,touch:ev.pointerType!=="mouse",moved:false};if(st.touch)st.timer=setTimeout(()=>{if(!st.moved&&drag===st)iniciar(st,st.x,st.y)},280);drag=st});
  e.addEventListener("click",()=>{if(!e._sup)abrir(l);e._sup=false});
  return e;
}
function ordenar(a,b){return (a.dataProximo||"9999")<(b.dataProximo||"9999")?-1:(a.dataProximo||"9999")>(b.dataProximo||"9999")?1:a.row-b.row}
function render(){
  renderStats(); renderOrigens();
  const v=visiveis(), board=$("#crmk-board"), sl=board.scrollLeft;
  const tops=[...board.querySelectorAll(".list")].map(x=>x.scrollTop);
  board.replaceChildren(...STAGES.map(([nome,tok])=>{
    const itens=v.filter(l=>l.etapa===nome||(nome==="Novo"&&!STAGES.some(s=>s[0]===l.etapa))).sort(ordenar);
    return el("section",{class:"col",style:`--c:var(${tok})`,"data-etapa":nome},
      el("div",{class:"col-h"},el("span",{class:"dot"}),el("h2",{},nome),el("span",{class:"n"},String(itens.length))),
      el("div",{class:"list"},itens.length?itens.map(card):el("div",{class:"empty"},"Arraste um lead para cá")));
  }));
  board.scrollLeft=sl; board.querySelectorAll(".list").forEach((x,i)=>{if(tops[i])x.scrollTop=tops[i]});
}

/* ---------- arrastar entre colunas ---------- */
function iniciar(st,x,y){
  st.active=true; const r=st.el.getBoundingClientRect(); st.dx=x-r.left; st.dy=y-r.top;
  st.ghost=st.el.cloneNode(true); st.ghost.classList.add("ghost"); st.ghost.style.width=r.width+"px"; root.append(st.ghost);
  st.el.classList.add("dragging"); st.ph=el("div",{class:"ph"}); try{navigator.vibrate&&navigator.vibrate(15)}catch(_){}
  mover(x,y);
}
function mover(x,y){
  const st=drag; st.ghost.style.left=(x-st.dx)+"px"; st.ghost.style.top=(y-st.dy)+"px";
  st.ghost.style.display="none"; const alvo=document.elementFromPoint(x,y); st.ghost.style.display="";
  const colEl=alvo&&alvo.closest("#crmk .col");
  root.querySelectorAll(".col.over").forEach(c=>c!==colEl&&c.classList.remove("over"));
  if(colEl){colEl.classList.add("over");const list=$(".list",colEl);const vazio=$(".empty",list);if(vazio)vazio.remove();st.ph.style.setProperty("--c",getComputedStyle(colEl).getPropertyValue("--c"));list.append(st.ph);st.col=colEl}
  const b=$("#crmk-board"),bb=b.getBoundingClientRect(); if(x>bb.right-50)b.scrollLeft+=14; else if(x<bb.left+50)b.scrollLeft-=14;
}
document.addEventListener("pointermove",ev=>{
  if(!drag||ev.pointerId!==drag.id)return; const d=Math.hypot(ev.clientX-drag.x,ev.clientY-drag.y);
  if(!drag.active){if(drag.touch){if(d>8){drag.moved=true;clearTimeout(drag.timer);drag=null}}else if(d>6)iniciar(drag,ev.clientX,ev.clientY);return}
  ev.preventDefault(); mover(ev.clientX,ev.clientY);
});
document.addEventListener("touchmove",ev=>{if(drag&&drag.active)ev.preventDefault()},{passive:false});
document.addEventListener("contextmenu",ev=>{if(drag&&drag.active)ev.preventDefault()});
document.addEventListener("pointercancel",()=>{if(drag){clearTimeout(drag.timer);if(drag.active){drag.ghost.remove();render()}drag=null}});
document.addEventListener("pointerup",async()=>{
  if(!drag)return; const st=drag; drag=null; clearTimeout(st.timer); if(!st.active)return;
  st.el._sup=true; setTimeout(()=>st.el._sup=false,50); st.ghost.remove();
  root.querySelectorAll(".col.over").forEach(c=>c.classList.remove("over"));
  const etapa=st.col&&st.col.dataset.etapa, l=st.lead;
  if(!etapa||etapa===l.etapa){render();return}
  const antes=l.etapa; l.etapa=etapa; render();
  await salvar(l,{etapa},()=>{l.etapa=antes},`${l.nome} → ${etapa}`);
});

/* ---------- gaveta de edição ---------- */
function abrir(l0){
  const novo=!l0; const l=novo?{nome:"",whatsapp:"",origem:"Google",entrada:hoje(),etapa:"Novo",ultimoContato:"",proximoPasso:"",dataProximo:"",obs:""}:Object.assign({},l0);
  const campo=(k,rot,tipo)=>el("div",{class:"f"},el("label",{for:"crmk-f-"+k},rot),el("input",{id:"crmk-f-"+k,type:tipo||"text",value:l[k]||""}));
  const sel=(k,rot,ops)=>{const s=el("select",{id:"crmk-f-"+k},...ops.map(o=>el("option",{value:o},o)));s.value=l[k]||ops[0];return el("div",{class:"f"},el("label",{for:"crmk-f-"+k},rot),s)};
  const r=novo?null:lemb(l);
  const salvarBtn=el("button",{class:"btn primary",type:"submit"},novo?"Adicionar na planilha":"Salvar na planilha");
  const form=el("form",{class:"drawer",role:"dialog","aria-modal":"true","aria-label":novo?"Novo lead":l.nome},
    el("h3",{},novo?"Novo lead":l.nome),
    novo?null:el("div",{class:"muted"},"Linha "+l.row+" da aba CRM"),
    waLink(l.whatsapp)?el("a",{class:"wa",href:waLink(l.whatsapp),target:"_blank",rel:"noopener"},"Abrir conversa no WhatsApp ↗"):null,
    novo?null:el("button",{class:"btn"+(r?" bellbtn":""),type:"button",html:ICON.bell+"<span>"+(r?r.tipo+" · "+quandoCurto(r):"Criar lembrete")+"</span>",onclick:()=>{fechar();abrirLembrete(l0)}}),
    campo("nome","Nome"),
    el("div",{class:"grid2"},campo("whatsapp","WhatsApp (DDD + número)","tel"),sel("origem","Origem",ORIGENS.includes(l.origem)||!l.origem?ORIGENS:[l.origem].concat(ORIGENS))),
    el("div",{class:"grid2"},sel("etapa","Etapa",STAGES.map(s=>s[0])),campo("entrada","Entrada","date")),
    campo("proximoPasso","Próximo passo"),
    el("div",{class:"grid2"},campo("dataProximo","Data do próximo passo","date"),campo("ultimoContato","Último contato","date")),
    el("div",{class:"f"},el("label",{for:"crmk-f-obs"},"Observações"),el("textarea",{id:"crmk-f-obs"},l.obs||"")),
    el("div",{class:"actions"},salvarBtn,el("button",{class:"btn",type:"button",onclick:fechar},"Fechar")));
  form.addEventListener("submit",async ev=>{ev.preventDefault();
    const d={}; ["nome","whatsapp","origem","etapa","entrada","proximoPasso","dataProximo","ultimoContato","obs"].forEach(k=>d[k]=$("#crmk-f-"+k,form).value.trim());
    d.whatsapp=d.whatsapp.replace(/\D/g,""); if(!d.nome){status("Coloque o nome do lead.",true);return}
    salvarBtn.disabled=true;
    try{ if(novo){await api({acao:"adicionar",campos:d});status("Lead adicionado na planilha")}
         else{await api({acao:"atualizar",row:l.row,nome:l0.nome,campos:d});status("Salvo na planilha")}
         fechar(); carregar(true);
    }catch(e){status("Não salvou: "+e.message,true);salvarBtn.disabled=false}
  });
  const bg=el("div",{class:"drawer-bg",onclick:ev=>{if(ev.target===bg)fechar()}},form);
  $("#crmk-drawer").replaceChildren(bg); $("#crmk-f-nome",form).focus();
}
function fechar(){$("#crmk-drawer").replaceChildren()}

/* ---------- pop-ups ---------- */
function abrirPop(conteudo,classe,aoFechar){
  const pop=el("div",{class:"pop "+(classe||""),role:"dialog","aria-modal":"true"},conteudo);
  const bg=el("div",{class:"pop-bg",onclick:ev=>{if(ev.target===bg)fecharPop()}},pop);
  bg._aoFechar=aoFechar; $("#crmk-pop").replaceChildren(bg); const f=pop.querySelector("input,button"); if(f)f.focus(); return pop;
}
function fecharPop(){const bg=$("#crmk-pop").firstChild; if(bg&&bg._aoFechar)bg._aoFechar(); $("#crmk-pop").replaceChildren()}
document.addEventListener("keydown",ev=>{if(ev.key==="Escape"){if($("#crmk-pop").firstChild)fecharPop();else fechar()}});

function abrirLembrete(l){
  const r=lemb(l); const now=new Date(); const sug=new Date(now.getTime()+36e5); sug.setMinutes(sug.getMinutes()<30?30:60,0,0);
  let tipo=r?r.tipo:"Chamar no WhatsApp";
  const dia=el("input",{id:"crmk-l-dia",type:"date",value:r?r.dia:isoDia(sug)});
  const hora=el("input",{id:"crmk-l-hora",type:"time",value:r?r.hora:pad(sug.getHours())+":"+pad(sug.getMinutes())});
  const nota=el("input",{id:"crmk-l-nota",type:"text",placeholder:"Ex.: perguntar se conseguiu ver o orçamento",value:r?r.nota:""});
  const tipos=el("div",{class:"tipos",role:"group","aria-label":"Tipo de lembrete"});
  const pintarTipos=()=>tipos.replaceChildren(...TIPOS.map(t=>el("button",{class:"chip",type:"button","aria-pressed":String(t===tipo),onclick:()=>{tipo=t;pintarTipos()}},t)));
  pintarTipos();
  const rap=(rot,fn)=>el("button",{class:"chip",type:"button",onclick:()=>{const d=fn();dia.value=isoDia(d);hora.value=pad(d.getHours())+":"+pad(d.getMinutes())}},rot);
  const em=min=>()=>new Date(Date.now()+min*6e4);
  const as=(diaMais,h)=>()=>{const d=new Date();d.setDate(d.getDate()+diaMais);d.setHours(h,0,0,0);return d};
  const salvarBtn=el("button",{class:"btn bellbtn",type:"submit",html:ICON.bell+"<span>Salvar lembrete</span>"});
  const form=el("form",{},
    el("div",{style:"display:flex;flex-direction:column;gap:12px"},
      el("h3",{},r?"Editar lembrete":"Novo lembrete"),
      el("div",{class:"who"},l.nome+(l.whatsapp?" · "+fone(l.whatsapp):"")),
      tipos,
      el("div",{class:"rapidos"},rap("Em 30 min",em(30)),rap("Em 1 h",em(60)),rap("Hoje 18h",as(0,18)),rap("Amanhã 9h",as(1,9)),rap("Amanhã 14h",as(1,14))),
      el("div",{class:"grid2"},el("div",{class:"f"},el("label",{for:"crmk-l-dia"},"Dia"),dia),el("div",{class:"f"},el("label",{for:"crmk-l-hora"},"Hora"),hora)),
      el("div",{class:"f"},el("label",{for:"crmk-l-nota"},"Nota (opcional)"),nota),
      el("div",{class:"actions"},salvarBtn,
        r?el("button",{class:"btn danger",type:"button",onclick:async()=>{fecharPop();l.lembrete="";await salvar(l,{lembrete:""},null,"lembrete removido")}},"Remover"):null,
        el("button",{class:"btn",type:"button",onclick:fecharPop},"Cancelar"))));
  form.addEventListener("submit",async ev=>{ev.preventDefault();
    if(!dia.value||!hora.value){status("Escolha o dia e a hora do lembrete.",true);return}
    pedirNotificacao(); destravarSom();
    const txt=textoLemb(dia.value,hora.value,tipo,nota.value.trim()); const antes=l.lembrete;
    salvarBtn.disabled=true; l.lembrete=txt; fecharPop();
    await salvar(l,{lembrete:txt},()=>{l.lembrete=antes},"lembrete "+quandoCurto(lemb(l)));
  });
  abrirPop(form);
}

function abrirLista(){
  const itens=leads.map(l=>({l,r:lemb(l)})).filter(x=>x.r).sort((a,b)=>a.r.quando-b.r.quando);
  abrirPop(el("div",{style:"display:flex;flex-direction:column;gap:12px"},
    el("h3",{},"Lembretes"),
    itens.length?el("div",{class:"lista-lemb"},itens.map(({l,r})=>el("div",{class:"lemb-item"+(vencido(r)?" passou":""),role:"button",tabindex:"0",onclick:()=>{fecharPop();abrirLembrete(l)}},
      el("b",{},quandoCurto(r)),el("div",{},el("div",{style:"font-weight:600"},l.nome),el("div",{class:"muted"},r.tipo+(r.nota?" · "+r.nota:"")))))):
      el("div",{class:"muted"},"Nenhum lembrete marcado. Toque no sino de um cartão para criar."),
    el("div",{class:"actions"},el("button",{class:"btn",type:"button",onclick:fecharPop},"Fechar"))));
}
$("#crmk-lembretes").addEventListener("click",abrirLista);

/* ---------- alerta na hora marcada ---------- */
const AVISADOS="crmk-avisados";
const jaAvisado=(l,r)=>{try{return(JSON.parse(ler(AVISADOS)||"[]")).includes(l.row+"|"+r.raw)}catch(_){return false}};
const marcarAvisado=(l,r)=>{let a=[];try{a=JSON.parse(ler(AVISADOS)||"[]")}catch(_){}a.push(l.row+"|"+r.raw);guardar(AVISADOS,JSON.stringify(a.slice(-200)))};
let ctx=null;
function destravarSom(){try{ctx=ctx||new (window.AudioContext||window.webkitAudioContext)();if(ctx.state==="suspended")ctx.resume()}catch(_){}}
document.addEventListener("pointerdown",destravarSom,{once:true});
function tocar(){try{if(!ctx)return;const t=ctx.currentTime;[[880,0],[1320,.18],[880,.6],[1320,.78]].forEach(([f,d])=>{const o=ctx.createOscillator(),g=ctx.createGain();o.type="sine";o.frequency.value=f;g.gain.setValueAtTime(0,t+d);g.gain.linearRampToValueAtTime(.25,t+d+.02);g.gain.exponentialRampToValueAtTime(.001,t+d+.5);o.connect(g).connect(ctx.destination);o.start(t+d);o.stop(t+d+.55)})}catch(_){}}
function pedirNotificacao(){try{if("Notification" in window&&Notification.permission==="default")Notification.requestPermission()}catch(_){}}
function notificar(l,r){try{if("Notification" in window&&Notification.permission==="granted"&&document.hidden){const n=new Notification(r.tipo+": "+l.nome,{body:(r.nota||l.proximoPasso||"")+" · "+r.hora,tag:"crmk-"+l.row,requireInteraction:true});n.onclick=()=>{window.focus();n.close()}}}catch(_){}}
let tituloOrig=document.title, piscar=null;
function piscarTitulo(txt){clearInterval(piscar);let on=false;piscar=setInterval(()=>{document.title=(on=!on)?"🔔 "+txt:tituloOrig},1000)}
function pararTitulo(){clearInterval(piscar);document.title=tituloOrig}

function checarLembretes(){
  if(emAlerta||drag&&drag.active)return;
  const prox=leads.map(l=>({l,r:lemb(l)})).filter(x=>x.r&&vencido(x.r)&&!jaAvisado(x.l,x.r)).sort((a,b)=>a.r.quando-b.r.quando)[0];
  if(!prox)return; mostrarAlerta(prox.l,prox.r);
}
function mostrarAlerta(l,r){
  emAlerta=true; marcarAvisado(l,r); fechar(); tocar(); notificar(l,r); piscarTitulo(l.nome);
  const link=waLink(l.whatsapp);
  const adiar=async min=>{const d=new Date(Date.now()+min*6e4);const txt=textoLemb(isoDia(d),pad(d.getHours())+":"+pad(d.getMinutes()),r.tipo,r.nota);l.lembrete=txt;fecharPop();await salvar(l,{lembrete:txt},null,"adiado para "+pad(d.getHours())+":"+pad(d.getMinutes()))};
  const pop=abrirPop(el("div",{style:"display:flex;flex-direction:column;gap:10px;align-items:center"},
    el("div",{class:"sino",html:ICON.bell}),
    el("div",{class:"quando"},"Lembrete · "+quandoCurto(r)),
    el("div",{class:"tipo"},r.tipo),
    el("h3",{},l.nome),
    l.whatsapp?el("div",{class:"who"},fone(l.whatsapp)):null,
    r.nota?el("div",{},r.nota):(l.proximoPasso?el("div",{class:"muted"},l.proximoPasso):null),
    el("div",{class:"actions"},
      link?el("a",{class:"btn primary",href:link,target:"_blank",rel:"noopener",style:"text-decoration:none"},"Abrir WhatsApp"):null,
      el("button",{class:"btn",type:"button",onclick:()=>adiar(10)},"Adiar 10 min"),
      el("button",{class:"btn",type:"button",onclick:()=>adiar(60)},"Adiar 1 h"),
      el("button",{class:"btn bellbtn",type:"button",onclick:async()=>{fecharPop();l.lembrete="";await salvar(l,{lembrete:""},null,"lembrete concluído")}},"Feito ✓"))),
    "alerta",()=>{emAlerta=false;pararTitulo();setTimeout(checarLembretes,800)});
  pop.animate&&pop.animate([{transform:"translateX(0)"},{transform:"translateX(-8px) rotate(-1deg)"},{transform:"translateX(8px) rotate(1deg)"},{transform:"translateX(-5px)"},{transform:"translateX(0)"}],{duration:500,delay:350});
}

/* ---------- inicialização ---------- */
$("#crmk-q").addEventListener("input",ev=>{busca=ev.target.value;render()});
$("#crmk-add").addEventListener("click",()=>abrir(null));
$("#crmk-reload").addEventListener("click",()=>carregar(false));
document.addEventListener("visibilitychange",()=>{if(!document.hidden){pararTitulo();if(Date.now()-ultimaCarga>15000)carregar(true)}});
setInterval(()=>{if(!document.hidden)carregar(true)},30000);
setInterval(()=>{if(leads.length){checarLembretes();if(!drag&&!$("#crmk-drawer").firstChild&&!$("#crmk-pop").firstChild)render()}},15000);
render(); carregar(true);
})();
