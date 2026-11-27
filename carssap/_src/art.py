# SVG 그림 도우미 (모두 직접 그린 도형)
BLUE='#2f7be0'; ORG='#ee6c3b'; NAVY='#14213d'; YEL='#ffd84d'
import json as _j
_S=_j.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'site_shapes.json'))); PROF=_S['P']; GEOM=_S['G']
_cid=[0]
def _smooth(pts):
    n=len(pts); mid=lambda p,q:((p[0]+q[0])/2,(p[1]+q[1])/2)
    s=mid(pts[-1],pts[0]); d=f'M{s[0]:.1f} {s[1]:.1f}'
    for i in range(n):
        p=pts[i]; m=mid(p,pts[(i+1)%n]); d+=f' Q{p[0]:.1f} {p[1]:.1f} {m[0]:.1f} {m[1]:.1f}'
    return d+'Z'
def t(x,y,sz,txt,fill='#13203a',anchor='start',w=900,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{sz}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{txt}</text>'
def car(x,ground,L,H,wb,kind,col,s,fo=.28,flip=False,sw=4.5,wheels=True,fill=None,stroke=None,wincol='#fff',winop=.6):
    k={'hatch':'hatch','suv':'suv','mpv':'mpv','sedan':'sedan','box':'box'}[kind]
    gm=GEOM[k]; g=gm['g']
    pts=[(x+p[0]*L*s, ground-(g+p[1]*(H-g))*s) for p in PROF[k]]
    d=_smooth(pts); _cid[0]+=1; cid=f'cw{_cid[0]}'
    fill=fill or col; stroke=stroke or col
    top=ground-H*s; belt=ground-gm['belt']*H*s
    x1=x+gm['glass'][0]*L*s; x2=x+gm['glass'][1]*L*s
    o=f'<defs><clipPath id="{cid}"><path d="{d}"/></clipPath></defs>'
    o+=f'<path d="{d}" fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o+=f'<rect x="{x1:.1f}" y="{top+H*s*.05:.1f}" width="{x2-x1:.1f}" height="{belt-top-H*s*.05:.1f}" fill="{wincol}" fill-opacity="{winop}" clip-path="url(#{cid})"/>'
    if wheels:
        r=gm['d']/2*s; fo_=(L-wb)*0.45
        for cx in (x+fo_*s, x+(fo_+wb)*s):
            cy=ground-r
            o+=f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#2d3340"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*.5:.1f}" fill="#cdd3df"/>'
    if flip: o=f'<g transform="translate({2*(x+L*s/2):.1f} 0) scale(-1 1)">{o}</g>'
    return o
def svg(vb_h,inner,vb_w=1000,vy=0):
    return f'<svg viewBox="0 {vy} {vb_w} {vb_h}" width="100%" style="display:block" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def legend(y,a,b,fs=64,ca=BLUE,cb=ORG,xa=70,xb=560,fill='#13203a'):
    return (f'<circle cx="{xa}" cy="{y-20}" r="20" fill="{ca}"/>'+t(xa+38,y,fs,a,ca)+
            f'<circle cx="{xb}" cy="{y-20}" r="20" fill="{cb}"/>'+t(xb+38,y,fs,b,cb))
def overlay(A,B,ka,kb,x0=70,ground=380,H=500,ls=True,names=None,fo=.2):
    s=860/max(A['L'],B['L'])
    hm=max(A['H'],B['H'])*s
    lo,hi=sorted([A['L'],B['L']])
    band=f'<rect x="{x0+lo*s:.1f}" y="{ground-hm:.1f}" width="{(hi-lo)*s:.1f}" height="{hm:.1f}" fill="{YEL}" fill-opacity=".9"/>'
    out=band+car(x0,ground,A['L'],A['H'],A['wb'],ka,BLUE,s,fo)+car(x0,ground,B['L'],B['H'],B['wb'],kb,ORG,s,fo)
    out+=f'<line x1="40" x2="960" y1="{ground}" y2="{ground}" stroke="#8a97b3" stroke-width="4"/>'
    if names: out+=legend(ground+85,names[0],names[1])
    return svg(H,out),s
def stack(A,B,ka,kb,names,x0=60):
    s=700/max(A['L'],B['L']); g1=300; g2=650
    lo,hi=sorted([A['L'],B['L']])
    out=f'<rect x="{x0+lo*s:.1f}" y="{g1-A["H"]*s-30:.1f}" width="{(hi-lo)*s:.1f}" height="{g2-g1+A["H"]*s+30:.1f}" fill="{YEL}" fill-opacity=".9"/>'
    out+=car(x0,g1,A['L'],A['H'],A['wb'],ka,BLUE,s,.14)+car(x0,g2,B['L'],B['H'],B['wb'],kb,ORG,s,.14)
    out+=f'<line x1="30" x2="970" y1="{g1}" y2="{g1}" stroke="#8a97b3" stroke-width="4"/><line x1="30" x2="970" y1="{g2}" y2="{g2}" stroke="#8a97b3" stroke-width="4"/>'
    for L in (A['L'],B['L']):
        out+=f'<line x1="{x0+L*s:.1f}" x2="{x0+L*s:.1f}" y1="{g1-A["H"]*s-40:.1f}" y2="{g2+10}" stroke="#13203a" stroke-width="3" stroke-dasharray="12 8"/>'
    out+=t(x0,g1-A['H']*s-48,62,names[0],BLUE)+t(x0,g2-B['H']*s-18,62,names[1],ORG)
    return svg(780,out,vy=-70)
def roofs(A,B,ka,kb,names):
    s=860/max(A['L'],B['L']); g=430
    out=car(70,g,A['L'],A['H'],A['wb'],ka,BLUE,s,.12)+car(70,g,B['L'],B['H'],B['wb'],kb,ORG,s,.12)
    for c,H in ((BLUE,A['H']),(ORG,B['H'])):
        y=g-H*s
        out+=f'<line x1="40" x2="960" y1="{y:.1f}" y2="{y:.1f}" stroke="{c}" stroke-width="5" stroke-dasharray="16 10"/>'
    out+=f'<line x1="40" x2="960" y1="{g}" y2="{g}" stroke="#8a97b3" stroke-width="4"/>'
    out+=legend(g+90,f'{names[0]} {A["H"]:,}',f'{names[1]} {B["H"]:,}',52)
    return svg(560,out)
def bars(a,b,ha,hb,ta,tb,na,nb,col_a=BLUE,col_b=ORG,base=520,top=120,fill='#13203a',vb=640,unit=''):
    mx=max(ha,hb); sc=(base-top-110)/mx
    out=f'<line x1="60" x2="940" y1="{base}" y2="{base}" stroke="#8a97b3" stroke-width="4"/>'
    for x,hv,c,tx,nm in ((160,ha,col_a,ta,na),(560,hb,col_b,tb,nb)):
        h=hv*sc
        out+=f'<rect x="{x}" y="{base-h:.1f}" width="280" height="{h:.1f}" rx="16" fill="{c}"/>'
        out+=t(x+140,base-h-22,88,tx,c,'middle')+t(x+140,base+66,62,nm,fill,'middle',900)
    return svg(vb,out)
def person(x,y,c='#14213d',k=1.6):
    return f'<circle cx="{x}" cy="{y}" r="{17*k:.1f}" fill="{c}"/><rect x="{x-18*k:.1f}" y="{y+22*k:.1f}" width="{36*k:.1f}" height="{42*k:.1f}" rx="{14*k:.1f}" fill="{c}"/>'
def topview(x,y,L,W,s,col,fo=.3):
    w=L*s;h=W*s
    o=f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h*.28:.1f}" fill="{col}" fill-opacity="{fo}" stroke="{col}" stroke-width="5"/>'
    o+=f'<rect x="{x+w*.58:.1f}" y="{y+h*.14:.1f}" width="{w*.16:.1f}" height="{h*.72:.1f}" rx="6" fill="#fff" fill-opacity=".6"/>'
    o+=f'<rect x="{x+w*.2:.1f}" y="{y+h*.16:.1f}" width="{w*.1:.1f}" height="{h*.68:.1f}" rx="6" fill="#fff" fill-opacity=".45"/>'
    for cx in (x+w*.2,x+w*.78):
        for cy in (y-5,y+h-h*.1):
            o+=f'<rect x="{cx-w*.06:.1f}" y="{cy:.1f}" width="{w*.12:.1f}" height="{h*.12+5:.1f}" rx="6" fill="#39414f"/>'
    return o
# ---- 실용 그림 (남색 배경용) ----
def padlock(cx,cy,sz,open_=False,c='#fff'):
    r=sz*.55
    arc=f'M{cx-r*.55} {cy-sz*.1} v{-sz*.35} a{r*.55} {r*.55} 0 0 1 {r*1.1} 0 v{ -sz*.0}' if not open_ else f'M{cx-r*.55} {cy-sz*.1} v{-sz*.35} a{r*.55} {r*.55} 0 0 1 {r*1.1} 0 v{-sz*.18}'
    return f'<path d="{arc}" fill="none" stroke="{c}" stroke-width="{sz*.14}" stroke-linecap="round"/><rect x="{cx-sz*.5}" y="{cy-sz*.12}" width="{sz}" height="{sz*.8}" rx="{sz*.14}" fill="{c}"/>'
def fob(cx,cy,sc=1,rot=0,body='#1d2b52',line=YEL,btns=True):
    o=f'<g transform="translate({cx},{cy}) rotate({rot}) scale({sc})"><rect x="-120" y="-215" width="240" height="430" rx="110" fill="{body}" stroke="{line}" stroke-width="9"/><circle cx="0" cy="-165" r="20" fill="none" stroke="{line}" stroke-width="8"/>'
    if btns:
        o+=f'<circle cx="0" cy="-60" r="52" fill="#2d4079" stroke="{line}" stroke-width="5"/>'+padlock(0,-60,40,False,'#fff')
        o+=f'<circle cx="0" cy="70" r="52" fill="#2d4079" stroke="{line}" stroke-width="5"/>'+padlock(0,70,40,True,'#fff')
        o+=f'<rect x="-48" y="150" width="96" height="40" rx="20" fill="#2d4079" stroke="{line}" stroke-width="5"/>'
    return o+'</g>'
def coin(cx,cy,r,plus=True,c='#d5dbe8'):
    o=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="#fff" stroke-width="6"/><circle cx="{cx}" cy="{cy}" r="{r*.82}" fill="none" stroke="#9aa6c2" stroke-width="4"/>'
    if plus: o+=f'<path d="M{cx-r*.35} {cy} H{cx+r*.35} M{cx} {cy-r*.35} V{cy+r*.35}" stroke="{NAVY}" stroke-width="{r*.16}" stroke-linecap="round"/>'
    return o
def num(x,y,n,r=34,fill=YEL,tc=NAVY):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'+t(x,y+r*.36,r*1.1,str(n),tc,'middle',900)
def battery(x,y,w=240,h=130,label='',c='#e8edf8'):
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#2d4079" stroke="{c}" stroke-width="6"/>'
    o+=f'<rect x="{x+30}" y="{y-26}" width="54" height="30" rx="6" fill="{c}"/><rect x="{x+w-84}" y="{y-26}" width="54" height="30" rx="6" fill="{c}"/>'
    o+=t(x+57,y-34,44,'+','#ff6b6b','middle')+t(x+w-57,y-34,44,'−','#e8edf8','middle')
    if label: o+=t(x+w/2,y+h*.62,46,label,'#fff','middle')
    return o
