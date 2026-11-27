import sys; sys.path.insert(0,'/home/claude/ig')
from art import *
GV={'L':4715,'H':1630,'wb':2875}; MY={'L':4790,'H':1624,'wb':2890}
CA={'L':5155,'H':1775,'wb':3090}; PA={'L':5060,'H':1805,'wb':2970}
h=open('/home/claude/ig/weekly.html').read()
CSS='''/* ---- 인스타 슬라이드 (4:5). 그림 위주. 글자는 슬라이드 폭 기준(cqw) ---- */
.slide{container-type:inline-size;aspect-ratio:4/5;border-radius:10px;overflow:hidden;position:relative;display:flex;flex-direction:column;padding:6% 7% 6%;font-family:var(--font);box-shadow:0 1px 3px rgba(0,0,0,.18);color:#13203a;background:#fff;min-width:0}
.slide *{min-width:0}
.slide>*+*{margin-top:2.5cqw}
.top{display:flex;justify-content:space-between;align-items:center;font-size:5.8cqw;font-weight:700;opacity:.85}
.big{font-size:13cqw;line-height:1.2;font-weight:900;letter-spacing:-.02em;text-wrap:balance}
.mid{font-size:10.4cqw;line-height:1.3;font-weight:900;text-wrap:balance;letter-spacing:-.02em}
.txt{font-size:6.6cqw;line-height:1.5;font-weight:700}
.sm{font-size:6.8cqw;line-height:1.45;font-weight:600;opacity:.9}
.foot{font-size:6.2cqw;font-weight:600;opacity:.85}
.art{flex:1;min-height:0;display:flex;align-items:center}
.art svg{width:100%;max-height:100%}
.cmp{background:linear-gradient(180deg,#e6f0ff 0%,#fff 62%)}
.cmp .a{color:#2f7be0}.cmp .b{color:#ee6c3b}
.prac{background:radial-gradient(120% 70% at 85% 0%,#2a3f7a 0%,#14213d 62%);color:#fff}
.prac .hl{color:#ffd84d}
.rank{background:radial-gradient(100% 60% at 15% 0%,#ffe98f 0%,#ffd84d 65%);color:#1a1a1a}
.cta{background:#2f7be0;color:#fff;border-radius:2.5cqw;padding:4cqw;font-size:6.8cqw;font-weight:900;text-align:center;line-height:1.35}
.prac .cta{background:#ffd84d;color:#14213d}
.rank .cta{background:#1a1a1a;color:#ffd84d}
.step{display:grid;grid-template-columns:11cqw 1fr;gap:3cqw;align-items:center;font-size:7.4cqw;line-height:1.3;font-weight:700}
.step i{font-style:normal;background:#ffd84d;color:#14213d;border-radius:50%;width:11cqw;height:11cqw;display:grid;place-items:center;font-weight:900;font-size:6.6cqw}
.warn{background:rgba(255,216,77,.16);border:1px solid rgba(255,216,77,.55);border-radius:2cqw;padding:3cqw;font-size:6.2cqw;line-height:1.4;font-weight:600}
'''
a=h.index('/* ---- 인스타 슬라이드'); b=h.index('</style>')
h=h[:a]+CSS+h[b:]
intro=h[h.index('</style>'):h.index('<section class="box"><h2>이번에 바꾼 점')]
k=h.index('<div class="box"><p class="note" style="margin-bottom:8px">'); k2=h.index('</pre>',k); cap=h[k:k2]+'</pre></div>'
tail=h[h.rindex('<section class="box">'):]
head=h[:h.index('</style>')]
def top(lbl,pg): return f'<div class="top"><span>{lbl}</span><span>{pg}/5</span></div>'
C='카쌉 · 자동차 크기 비교';P='카쌉 · 차 실용 정보';R='카쌉 · 숫자로 보는 자동차'
def S(cls,inner): return f'<div class="slide {cls}">{inner}</div>'
def art(x): return f'<div class="art">{x}</div>'
# ===== 월 =====
ov,_=overlay(GV,MY,'suv','suv',names=('GV70','모델 Y'))
m=[S('cmp',top(C,1)+'<div class="big">GV70 vs 모델 Y<br>크기 겹쳐 보기</div>'+art(ov)),
 S('cmp',top(C,2)+'<div class="mid">길이는 모델 Y가<br><span class="b">7.5cm</span> 더 길어요</div>'+art(stack(GV,MY,'suv','suv',('GV70','모델 Y')))+'<div class="sm">노란 부분이 길이 차이예요</div>'),
 S('cmp',top(C,3)+'<div class="mid">높이는<br><span class="a">거의 같아요</span></div>'+art(roofs(GV,MY,'suv','suv',('GV70','모델 Y')))+'<div class="sm">높이 차이는 6mm뿐이에요</div>'),
 S('cmp',top(C,4)+'<div class="mid">1년 연료비는<br><span class="b">3배 넘게</span> 차이</div>'+art(bars(0,0,284,87,'284만','87만','GV70 휘발유','모델 Y 전기'))+'<div class="sm">연 15,000km, 공인 연비·전비 기준</div>'),
 S('cmp',top(C,5)+'<div class="mid">내가 고민하는<br>두 차도 겹쳐 보세요</div>'+art(overlay(GV,MY,'suv','suv',fo=.18)[0])+'<div class="cta">프로필 링크 · 카쌉에서 확인</div>')]
# ===== 화 =====
big_fob=svg(560,fob(420,290,1.0,-12)+coin(790,170,95)+f'<path d="M700 260 Q650 330 600 330" fill="none" stroke="{YEL}" stroke-width="8" stroke-linecap="round" stroke-dasharray="4 18"/>')
def icon_col(cx,body,l1,l2):
    return body+t(cx,362,58,l1,'#fff','middle')+t(cx,428,58,l2,'#fff','middle')
ic1=car(60,235,3600,1500,2450,'box','#dfe5f1',.075,.9,sw=2,stroke='#9aa6c2')+padlock(200,110,60,False,YEL)
ic2=f'<circle cx="500" cy="190" r="100" fill="#2d4079" stroke="{YEL}" stroke-width="8"/><circle cx="500" cy="190" r="70" fill="none" stroke="#e8edf8" stroke-width="5"/>'+t(500,205,40,'START','#fff','middle')
ic3=battery(740,150,180,100,'')+t(830,222,70,'!',YEL,'middle')
p1=[S('prac',top(P,1)+'<div class="big">스마트키 배터리,<br><span class="hl">직접 갈아요</span></div>'+art(big_fob)+'<div class="foot">저장해 두면 급할 때 찾아요</div>'),
 S('prac',top(P,2)+'<div class="mid">이런 신호가 오면<br><span class="hl">교체 시기</span></div>'+art(svg(450,icon_col(190,ic1,'문이 잘','안 열려요')+icon_col(500,ic2,'시동 버튼','반응 느림')+icon_col(830,ic3,'계기판에','배터리 알림')))+'<div class="sm">알림 표시는 차종마다 달라요</div>'),
 S('prac',top(P,3)+'<div class="mid">교체 방법 1, 2</div>'+art(svg(380,fob(260,200,.78,0)+f'<rect x="440" y="170" width="300" height="34" rx="10" fill="#e8edf8"/><rect x="440" y="160" width="60" height="54" rx="10" fill="#cfd6e4"/>'+num(580,120,1)+coin(850,260,60,False)+f'<path d="M820 215 L780 150" stroke="{YEL}" stroke-width="8" stroke-linecap="round"/>'+num(850,150,2)))+'<div class="step"><i>1</i><span>버튼 누르고 비상키를 빼요</span></div><div class="step"><i>2</i><span>틈에 동전을 넣어 열어요</span></div>'),
 S('prac',top(P,4)+'<div class="mid">교체 방법 3, 4</div>'+art(svg(380,coin(300,190,130)+t(300,150,60,'+면 위로','#14213d','middle',900,'transform="translate(0,0)"')[:0]+f'<path d="M470 190 H620" stroke="{YEL}" stroke-width="10" stroke-linecap="round"/><path d="M600 160 L640 190 L600 220" fill="none" stroke="{YEL}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'+f'<rect x="680" y="100" width="260" height="180" rx="40" fill="#1d2b52" stroke="{YEL}" stroke-width="8"/>'+coin(810,190,56)+num(300,50,3)+num(810,40,4)))+'<div class="step"><i>3</i><span>같은 규격, +면 위로 갈아요</span></div><div class="step"><i>4</i><span>덮개를 닫고 작동 확인</span></div>'),
 S('prac',top(P,5)+'<div class="mid">이미 방전됐다면<br><span class="hl">키를 버튼에 대요</span></div>'+art(svg(440,f'<circle cx="680" cy="220" r="140" fill="#2d4079" stroke="{YEL}" stroke-width="9"/><circle cx="680" cy="220" r="102" fill="none" stroke="#e8edf8" stroke-width="6"/>'+t(680,238,56,'START','#fff','middle')+fob(280,230,.78,70)+f'<path d="M470 215 H510 M470 255 H515 M470 175 H510" stroke="{YEL}" stroke-width="9" stroke-linecap="round"/>'))+'<div class="warn">방법은 차종마다 달라요. 사용설명서를 확인하세요.</div><div class="cta">차 고를 땐 프로필 링크 카쌉</div>')]
# ===== 수 =====
RK='#c0392b'
def rowsvg(rows,hi=None):
    o='';
    for i,(rk,nm,v,L,H,wb,kd) in enumerate(rows):
        y=i*170+10
        if hi==i: o+=f'<rect x="10" y="{y}" width="980" height="160" rx="26" fill="#fff" fill-opacity=".55"/>'
        o+=f'<circle cx="64" cy="{y+80}" r="36" fill="#1a1a1a"/>'+t(64,y+96,42,rk,YEL,'middle')
        o+=car(105,y+135,L,H,wb,kd,'#f7f7f7',.058,.95,sw=2.5,stroke='#444')
        o+=t(395,y+98,42 if len(nm)>6 else 60,nm,'#1a1a1a')+t(975,y+102,86,f'{v}만','#1a1a1a','end')
    return svg(len(rows)*170+10,o)
rows=[(1,'모닝',240,3595,1485,2400,'box'),(2,'티볼리',249,4225,1615,2600,'suv'),(3,'트랙스 크로스오버',265,4540,1560,2700,'suv'),(4,'캐스퍼',270,3595,1575,2400,'box'),(5,'레이',271,3595,1700,2520,'box'),('+','아반떼',271,4765,1425,2750,'sedan')]
s=860/4765
cov=car(70,380,3595,1485,2400,'box',RK,s,.1,sw=5)+car(70,380,4765,1425,2750,'sedan',NAVY,s,.08,sw=5)+f'<line x1="40" x2="960" y1="380" y2="380" stroke="#1a1a1a" stroke-opacity=".5" stroke-width="4"/>'+legend(465,'모닝','아반떼',66,RK,NAVY)
sv=.14; tv=topview(120,90,3595,1595,sv,RK,.3)+topview(120,440,4765,1855,sv,NAVY,.25)+t(120,70,64,'모닝 5.73㎡',RK)+t(120,415,64,'아반떼 8.84㎡',NAVY)
r=[S('rank',top(R,1)+'<div class="big">같은 돈이면<br>어떤 차가 클까?</div>'+art(svg(520,cov))+'<div class="sm">1㎡당 시작가로 줄 세웠어요</div>'),
 S('rank',top(R,2)+'<div class="mid">1㎡당 시작가<br>낮은 차 TOP 3</div>'+art(rowsvg(rows[:3]))+'<div class="sm">면적 1㎡당 시작가 (만 원)</div>'),
 S('rank',top(R,3)+'<div class="mid">4위부터는 이래요</div>'+art(rowsvg(rows[3:],2))+'<div class="sm">아반떼가 레이와 같은 값이에요</div>'),
 S('rank',top(R,4)+'<div class="mid">모닝에서 아반떼로<br>면적이 <b>54%</b> 커져요</div>'+art(svg(740,tv))+'<div class="sm">위에서 본 크기, 같은 비율</div>'),
 S('rank',top(R,5)+'<div class="mid">시작가 차이는<br>1,023만 원이에요</div>'+art(bars(0,0,1375,2398,'1,375만','2,398만','모닝','아반떼',RK,NAVY,fill='#1a1a1a'))+'<div class="cta">144대 순위는 프로필 링크 카쌉</div>')]
# ===== 금 =====
def cable(d,col,w=11,under=True):
    o=''
    if under: o+=f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w+6}" stroke-linecap="round"/>' if col=='#111' else ''
    return o+f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
cars2=car(40,330,4700,1425,2750,'sedan','#dfe5f1',.105,.9,flip=True,sw=2,stroke='#9aa6c2')+car(500,330,4715,1630,2875,'suv','#dfe5f1',.105,.9,sw=2,stroke='#9aa6c2')
cars2+=cable('M300 190 Q500 60 640 190','#ff5c5c')+cable('M330 205 Q520 120 700 205','#111')+t(500,30,0,'','#fff')
bat_l=battery(80,150,260,140,'방전')+f'<circle cx="190" cy="350" r="18" fill="#9aa6c2"/>'+t(190,420,40,'금속 부분','#cfd6e4','middle',600)
bat_r=battery(660,150,260,140,'정상')
j3=svg(400,bat_l+bat_r+cable('M110 124 Q500 -10 690 124','#ff5c5c')+num(110,100,1)+num(690,100,2),vy=40)
j4=svg(400,bat_l+bat_r+cable('M110 124 Q500 -10 690 124','#ff5c5c',9)+cable('M890 124 Q900 400 190 350','#111')+num(890,100,3)+num(220,335,4,30),vy=40)
icn1=f'<circle cx="170" cy="150" r="90" fill="#2d4079" stroke="{YEL}" stroke-width="8"/>'+f'<rect x="150" y="100" width="40" height="70" rx="12" fill="#e8edf8"/><rect x="145" y="150" width="50" height="50" rx="10" fill="#e8edf8"/>'
icn2=f'<rect x="440" y="95" width="70" height="120" rx="12" fill="#ff5c5c"/><rect x="530" y="95" width="70" height="120" rx="12" fill="#111" stroke="#fff" stroke-width="6"/>'+t(475,175,70,'+','#fff','middle')+t(565,170,70,'−','#fff','middle')
icn3=car(690,215,3600,1500,2450,'box','#dfe5f1',.04,.9,sw=2,stroke='#9aa6c2')+car(840,215,3600,1500,2450,'box','#dfe5f1',.04,.9,flip=True,sw=2,stroke='#9aa6c2')
def ic3col(cx,body,l1,l2): return body+t(cx,362,58,l1,'#fff','middle')+t(cx,428,58,l2,'#fff','middle')
done=car(40,300,4715,1630,2875,'suv','#dfe5f1',.12,.9,sw=2,stroke='#9aa6c2')+''.join(f'<circle cx="{40-i*0}" cy="0" r="0"/>' for i in range(0))
puff=''.join(f'<circle cx="{40-i*34}" cy="{255-i*10}" r="{14+i*8}" fill="#e8edf8" fill-opacity="{.7-i*.15}"/>' for i in range(4))
j5=svg(420,done+puff+f'<line x1="20" x2="980" y1="300" y2="300" stroke="#9aa6c2" stroke-width="4"/>'+num(700,90,4)+num(790,90,3)+num(880,90,2)+num(960,90,1)+f'<path d="M670 150 H980" stroke="{YEL}" stroke-width="8" stroke-linecap="round"/>')
p2=[S('prac',top(P,1)+'<div class="big">시동이 안 걸려요<br><span class="hl">점프 연결 순서</span></div>'+art(svg(480,cars2+t(190,400,60,'방전','#fff','middle')+t(810,400,60,'정상','#fff','middle')))+'<div class="foot">저장해 두세요</div>'),
 S('prac',top(P,2)+'<div class="mid">연결 전에<br><span class="hl">이 3가지</span></div>'+art(svg(450,ic3col(170,icn1,'두 차 모두','시동 끄기')+ic3col(520,icn2,'빨강 +','검정 −')+ic3col(830,icn3,'두 차를','가깝게')))+'<div class="warn">전기차, 하이브리드는 방법이 달라요. 사용설명서를 먼저 보세요.</div>'),
 S('prac',top(P,3)+'<div class="mid">빨간 케이블<br>1 방전 차 +, 2 정상 차 +</div>'.replace('<br>1 방전 차 +, 2 정상 차 +','')+art(j3)+'<div class="step"><i>1</i><span>빨강을 방전 차 + 단자에</span></div><div class="step"><i>2</i><span>반대쪽은 정상 차 + 단자에</span></div>'),
 S('prac',top(P,4)+'<div class="mid">검정 케이블</div>'+art(j4)+'<div class="step"><i>3</i><span>검정을 정상 차 − 단자에</span></div><div class="step"><i>4</i><span>반대쪽은 방전 차 금속에</span></div>'),
 S('prac',top(P,5)+'<div class="mid">시동이 걸리면<br><span class="hl">거꾸로 분리</span></div>'+art(j5)+'<div class="sm">4→1 순서로 떼고 잠시 주행</div><div class="cta">차 고를 땐 프로필 링크 카쌉</div>')]
# ===== 토 =====
ov2,_=overlay(CA,PA,'mpv','suv',names=('카니발','팰리세이드'))
seat=''.join(person(110+i*130,120,BLUE) for i in range(7))+''.join(person(100+i*100,360,ORG) for i in range(9))
seat=svg(500,seat+t(60,60,60,'7인승',BLUE)+t(60,300,60,'9인승',ORG))
tl=[S('cmp',top(C,1)+'<div class="big">카니발 vs<br>팰리세이드</div>'+art(ov2)),
 S('cmp',top(C,2)+'<div class="mid">길이는 카니발이<br><span class="a">9.5cm</span> 더 길어요</div>'+art(stack(CA,PA,'mpv','suv',('카니발','팰리세이드')))+'<div class="sm">노란 부분이 길이 차이예요</div>'),
 S('cmp',top(C,3)+'<div class="mid">높이는 팰리세이드가<br><span class="b">3cm</span> 더 높아요</div>'+art(roofs(CA,PA,'mpv','suv',('카니발','팰리세이드')))+'<div class="sm">점선이 지붕 높이예요</div>'),
 S('cmp',top(C,4)+'<div class="mid">시작가는<br><span class="b">792만 원</span> 차이</div>'+art(bars(0,0,3686,4478,'3,686만','4,478만','카니발','팰리세이드'))+'<div class="sm">휘발유 모델 시작가끼리 비교예요</div>'),
 S('cmp',top(C,5)+'<div class="mid">둘 다 7인승,<br>9인승이 있어요</div>'+art(seat)+'<div class="cta">프로필 링크 · 카쌉에서 확인</div>')]
def post(day,tag,tc,note,slides,extra=''):
    return f'<section class="post"><div class="post-head"><span class="day">{day}</span><span class="tag {tc}">{tag}</span><span class="note">{note}</span></div><div class="slides">{"".join(slides)}</div>{extra}</section>'
note='<section class="box"><h2>이번에 바꾼 점</h2><p class="note">글자보다 그림이 먼저 보이게 바꿨어요. 격자는 없앴고, 크기 비교는 실제 크기 비율로 그린 차 그림이 중심이에요. 실용 정보와 숫자 순위에도 직접 그린 그림을 넣었어요.</p></section>'
main=post('월','크기 비교','t-cmp','GV70 vs 모델 Y',m,cap)+post('화','실용 정보','t-prac','스마트키 배터리 교체',p1)+post('수','숫자 순위','t-rank','같은 돈으로 더 큰 차',r)+post('금','실용 정보','t-prac','배터리 방전 점프',p2)+post('토','크기 비교','t-cmp','카니발 vs 팰리세이드',tl)
open('/home/claude/ig/weekly3.html','w').write(head+intro+note+main+tail)
print('built')
