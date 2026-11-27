"""검수 페이지(아티팩트용 HTML) 생성. 승인은 2단계(승인 → 네, 승인할게요). 시트 '게시' 탭 상태를 직접 바꾼다.
posts: [{num, day, kind, title, caption, when('2026-11-30 10:00'), thumbs:[data URI...]}]
publish 때 capabilities: {"mcp": {"servers": [{"server": "Google Sheets", "tools": ["get_values", "update_values"]}]}}"""
import json, html

def build(posts, sheet_id, week_label):
    data = json.dumps({'posts': posts, 'sheet': sheet_id, 'week': week_label}, ensure_ascii=False).replace('<', '\\u003c')
    return PAGE.replace('__DATA__', data).replace('__WEEK__', html.escape(week_label))

PAGE = r'''<title>카쌉 주간 검수</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root{--bg:#f3f4f6;--fg:#14171f;--muted:#5d6472;--line:#d9dce3;--card:#fff;--acc:#2f7be0;--ok:#1f8f4e;--warn:#c0392b;--amber:#f2c14e}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0e1117;--fg:#eef0f5;--muted:#9aa2b2;--line:#262b36;--card:#171b24;--acc:#6aa6f2;--ok:#4cc07f;--warn:#ff7a6b;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0e1117;--fg:#eef0f5;--muted:#9aa2b2;--line:#262b36;--card:#171b24;--acc:#6aa6f2;--ok:#4cc07f;--warn:#ff7a6b;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:'Noto Sans KR',system-ui,sans-serif;margin:0;padding-block:20px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:18px}
h1{font-size:20px;margin:0}.sub{margin:4px 0 0;color:var(--muted);font-size:14px;line-height:1.55}
.post{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:10px;min-width:0}
.hd{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}.day{font-weight:900}.kind{font-size:12px;color:var(--muted)}
.st{margin-left:auto;font-size:12px;font-weight:700;padding:2px 8px;border-radius:99px;border:1px solid var(--line)}
.st.ok{color:var(--ok);border-color:var(--ok)}.st.bad{color:var(--warn);border-color:var(--warn)}
.ti{font-size:16px;font-weight:700;line-height:1.4;margin:0;word-break:keep-all}
.cv{position:relative}.car{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:8px;scrollbar-width:none;-webkit-overflow-scrolling:touch;border-radius:10px}.car::-webkit-scrollbar{display:none}.car img{flex:0 0 100%;width:100%;aspect-ratio:4/5;object-fit:cover;scroll-snap-align:center;border-radius:10px;display:block}.cnt{position:absolute;right:10px;top:10px;background:rgba(0,0,0,.6);color:#fff;font-size:13px;font-weight:700;padding:3px 10px;border-radius:99px}.nav{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;border:0;background:rgba(0,0,0,.45);color:#fff;font-size:22px;padding:0;min-height:0}.nav.l{left:8px}.nav.r{right:8px}.dots{display:flex;gap:6px;justify-content:center;margin-top:8px}.dots i{width:7px;height:7px;border-radius:50%;background:var(--line)}.dots i.on{background:var(--acc)}.row button{flex:1;min-height:52px;font-size:16px}
details{font-size:13px;color:var(--muted)}details pre{white-space:pre-wrap;word-break:break-word;margin:6px 0 0;font:inherit;color:var(--fg);line-height:1.6}
.row{display:flex;gap:8px;flex-wrap:wrap}
button{font:inherit;font-size:14px;font-weight:700;padding:10px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer;min-height:44px}
button.p{background:var(--acc);border-color:var(--acc);color:#fff}button.g{background:var(--ok);border-color:var(--ok);color:#fff}
button.w{color:var(--warn);border-color:var(--warn)}button:disabled{opacity:.5;cursor:default}
.box{border:1px solid var(--amber);background:color-mix(in srgb,var(--amber) 14%,transparent);border-radius:8px;padding:10px;font-size:14px;line-height:1.55}
textarea{width:100%;box-sizing:border-box;font:inherit;border:1px solid var(--line);border-radius:8px;padding:8px;background:var(--bg);color:var(--fg);min-height:60px}
.msg{font-size:13px;color:var(--muted);line-height:1.5}.msg.err{color:var(--warn)}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.88);display:none;align-items:center;justify-content:center;padding:12px;z-index:9}#lb img{max-width:100%;max-height:100%;border-radius:6px}
</style>
<div class="wrap">
<header><h1>카쌉 인스타 주간 검수</h1><p class="sub">__WEEK__ · 글마다 카드와 문구를 확인하고 승인하세요. 승인하면 정해진 요일 10시에 올라가요. 승인하지 않은 글은 올라가지 않아요.</p></header>
<div id="all"></div><div id="list" class="wrap" style="gap:14px"></div><p id="net" class="msg"></p></div>
<div id="lb"><img alt=""></div>
<script type="application/json" id="d">__DATA__</script>
<script>
(function(){
var D=JSON.parse(document.getElementById('d').textContent), SRV='Google Sheets', rows={}, mcp=null, pend={};
var E=function(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
var list=document.getElementById('list'), net=document.getElementById('net'), all=document.getElementById('all');
function say(m,err){net.textContent=m||'';net.className='msg'+(err?' err':'')}
function parse(res){var p=res&&res.payload; if(typeof p==='string'){try{p=JSON.parse(p)}catch(e){}} if(p&&p.values)return p.values; if(Array.isArray(p))return p; if(p&&p.valueRanges&&p.valueRanges[0])return p.valueRanges[0].values||[]; return null}
async function load(){
  if(!mcp){say('시트 연결을 사용할 수 없는 화면이에요. claude.ai에서 열어 주세요.',true);draw();return}
  try{var r=await mcp.callTool(SRV,'get_values',{spreadsheetId:D.sheet,range:'게시!A1:K200'},{cache:false}); var v=parse(r); if(!v)throw {code:'shape'};
    rows={}; for(var i=1;i<v.length;i++){var n=String(v[i][0]||'').trim(); if(n)rows[n]={row:i+1,status:v[i][1]||'',memo:v[i][9]||''}} say('');draw()}
  catch(e){say(e.code==='needs_reauth'?'구글 시트 연결이 만료됐어요. claude.ai 설정의 커넥터에서 다시 연결해 주세요.':e.code==='server_not_connected'?'구글 시트 커넥터가 연결돼 있지 않아요.':e.code==='not_in_manifest'||e.code==='approval_required'?'이 페이지의 시트 접근이 허용되지 않았어요. 다시 열어 허용해 주세요.':'시트 상태를 읽지 못했어요('+(e.code||'오류')+').',true);draw()}
}
async function setStatus(n,status,memo){
  var r=rows[n]; if(!r){say('시트에서 #'+n+' 글을 찾지 못했어요.',true);return false}
  try{await mcp.callTool(SRV,'update_values',{spreadsheetId:D.sheet,range:'게시!B'+r.row,values:[[status]]},{cache:false});
    if(memo!=null)await mcp.callTool(SRV,'update_values',{spreadsheetId:D.sheet,range:'게시!J'+r.row,values:[[memo]]},{cache:false});
    r.status=status; if(memo!=null)r.memo=memo; return true}
  catch(e){say('저장하지 못했어요('+(e.code||'오류')+'). 시트에서 직접 바꿔도 돼요.',true);return false}
}
function badge(s){var b=E('span','st',s||'확인 중'); if(s==='승인'||s==='게시완료')b.className+=' ok'; if(s==='반려'||s==='오류')b.className+=' bad'; return b}
function dayOf(w){return w}
function card(p){
  var r=rows[p.num], s=r?r.status:'', el=E('section','post'), h=E('div','hd');
  h.append(E('span','day',p.day),E('span','kind',p.kind+' · '+p.when+' 게시'),badge(s)); el.append(h,E('p','ti','#'+p.num+' '+p.title));
  var cv=E('div','cv'), car=E('div','car'), cnt=E('span','cnt','1/'+p.thumbs.length), dots=E('div','dots'), ds=[];
  p.thumbs.forEach(function(u,k){var i=E('img');i.src=u;i.alt='카드 '+(k+1);car.append(i);var d=E('i');if(!k)d.className='on';ds.push(d);dots.append(d)});
  function go(k){var w=car.clientWidth+8;k=Math.max(0,Math.min(p.thumbs.length-1,k));car.scrollTo({left:k*w,behavior:'smooth'})}
  car.addEventListener('scroll',function(){var w=car.clientWidth+8,k=Math.round(car.scrollLeft/w);cnt.textContent=(k+1)+'/'+p.thumbs.length;ds.forEach(function(d,j){d.className=j===k?'on':''})});
  var bl=E('button','nav l','‹'),br=E('button','nav r','›');bl.onclick=function(){go(Math.round(car.scrollLeft/(car.clientWidth+8))-1)};br.onclick=function(){go(Math.round(car.scrollLeft/(car.clientWidth+8))+1)};
  cv.append(car,cnt,bl,br); el.append(cv,dots);
  var d=E('details'); d.append(E('summary',null,'캡션 보기 (눌러서 펼치기)')); var pre=E('pre',null,p.caption); d.append(pre); el.append(d);
  var act=E('div','row'), pd=pend[p.num];
  if(!r){act.append(E('span','msg','시트 상태를 불러오는 중이거나 읽지 못했어요.'))}
  else if(s==='게시완료'){act.append(E('span','msg','이미 올라간 글이에요.'))}
  else if(pd==='approve'){var b=E('div','box','승인하면 '+p.when+'에 자동으로 올라가요.'); var y=E('button','g','네, 승인할게요'), n=E('button',null,'아니요'); y.onclick=async function(){y.disabled=true;if(await setStatus(p.num,'승인','')){delete pend[p.num]} draw()}; n.onclick=function(){delete pend[p.num];draw()}; act.append(b); var rr=E('div','row'); rr.append(y,n); el.append(act,rr); return el}
  else if(pd==='reject'){var ta=E('textarea'); ta.placeholder='반려 이유를 적어 주세요(다음 주 수정에 써요)'; var y2=E('button','w','반려하기'), n2=E('button',null,'취소'); y2.onclick=async function(){y2.disabled=true;if(await setStatus(p.num,'반려',ta.value||'반려')){delete pend[p.num]} draw()}; n2.onclick=function(){delete pend[p.num];draw()}; var rr2=E('div','row'); rr2.append(y2,n2); el.append(ta,rr2); return el}
  else if(s==='승인'){var c=E('button',null,'승인 취소'); c.onclick=async function(){c.disabled=true;await setStatus(p.num,'검수대기','');draw()}; act.append(c)}
  else{var a=E('button','p','승인'), x=E('button','w','반려'); a.onclick=function(){pend[p.num]='approve';draw()}; x.onclick=function(){pend[p.num]='reject';draw()}; act.append(a,x)}
  el.append(act); if(r&&r.memo&&s==='반려')el.append(E('p','msg','반려 이유: '+r.memo)); return el}
function draw(){
  list.textContent=''; all.textContent='';
  var open=D.posts.filter(function(p){var r=rows[p.num];return r&&r.status==='검수대기'});
  if(open.length>1){ if(pend.__all){var b=E('div','box','남은 '+open.length+'개 글을 모두 승인해요. 각 글은 정해진 요일 10시에 올라가요.'),y=E('button','g','네, 모두 승인할게요'),n=E('button',null,'아니요'); y.onclick=async function(){y.disabled=true;for(var i=0;i<open.length;i++){await setStatus(open[i].num,'승인','')} delete pend.__all;draw()}; n.onclick=function(){delete pend.__all;draw()}; var rr=E('div','row'); rr.style.marginTop='8px'; rr.append(y,n); all.append(b,rr)} else {var a=E('button','p','남은 '+open.length+'개 한 번에 승인'); a.onclick=function(){pend.__all=1;draw()}; all.append(a)} }
  D.posts.forEach(function(p){list.append(card(p))})
}
document.getElementById('lb').onclick=function(){this.style.display='none'};
draw();
if(window.claude&&claude.use){claude.use('mcp').then(function(m){mcp=m;load()}).catch(function(){load()})}
})();
</script>'''
