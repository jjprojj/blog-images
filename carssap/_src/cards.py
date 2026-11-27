"""카쌉 인스타 카드 합성 (1080x1350 JPEG). 사진 카드(실용/순위)와 크기 비교 SVG 카드."""
import base64, os, io, sys
sys.path.insert(0, os.path.dirname(__file__))
from art import *  # svg 도우미 (car, overlay, stack, roofs, bars, t ...)
D = os.path.dirname(__file__)
CSS = open(os.path.join(D, 'card.css')).read()
LOGO = open(os.path.join(D, 'logo.b64')).read()

def b64jpg(path):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode()

def go_tag(text='카쌉에서 확인'):
    return f'<span class="go"><img src="{LOGO}" alt="">{text}</span>'

def photo_cover(photo, label, kick, hd, dk='', foot='당황하지 말고', hd_cls='', cta='카쌉에서 확인'):
    """실용 정보 표지. hd는 <br>로 줄 나눔, 강조는 <em>"""
    dkh = f'<div class="dk">{dk}</div>' if dk else ''
    return (f'<div class="card" style="background-image:url(\'{b64jpg(photo)}\')"><div class="in">'
            f'<div class="mast"><b>CARSSAP</b><span>{label}</span></div><div class="kick">{kick}</div>'
            f'<div class="hd {hd_cls}">{hd}</div>{dkh}<div class="ft"><span>{foot}</span>{go_tag(cta)}</div></div></div>')

def photo_steps(photo, page, kick, hd, steps, note='차종마다 달라요. 사용설명서 확인'):
    st = ''.join(f'<div class="st"><i>{i+1}</i><span>{s}</span></div>' for i, s in enumerate(steps))
    return (f'<div class="card blur" style="background-image:url(\'{b64jpg(photo)}\')"><div class="in">'
            f'<div class="mast"><b>CARSSAP</b><span>{page}</span></div><div class="kick">{kick}</div>'
            f'<div class="hd s">{hd}</div><div class="panel">{st}</div><div class="ft"><span>{note}</span></div></div></div>')

def photo_rank_cover(photo, topn, sub, hd):
    return (f'<div class="card" style="background-image:url(\'{b64jpg(photo)}\')"><div class="in">'
            f'<div class="mast"><b>CARSSAP</b><span>숫자로 보는 자동차</span></div>'
            f'<div class="num">TOP<small>{topn}</small></div><div class="kick" style="margin-top:3cqw">{sub}</div>'
            f'<div class="hd m">{hd}</div><div class="ft"><span class="go" style="margin-left:auto"><img src="{LOGO}" alt="">세상 쉬운 차 비교 카쌉</span></div></div></div>')

def photo_big(photo, page, kick, hd, sub='', blur=False):
    """장면 카드: 큰 글자 한 줄 + 보조 문장"""
    s = f'<div class="dk">{sub}</div>' if sub else ''
    return (f'<div class="card{" blur" if blur else ""}" style="background-image:url(\'{b64jpg(photo)}\')"><div class="in">'
            f'<div class="mast"><b>CARSSAP</b><span>{page}</span></div><div class="kick">{kick}</div>'
            f'<div class="hd m">{hd}</div>{s}</div></div>')

def slide(cls, inner):
    return f'<div class="slide {cls}">{inner}</div>'
def top(lbl, pg, n=5):
    return f'<div class="top"><span>{lbl}</span><span>{pg}/{n}</span></div>'
def art_box(x):
    return f'<div class="art">{x}</div>'

def render(cards, outdir, width=1080):
    """cards: HTML 문자열 목록 → outdir/01.jpg ... (1080x1350, JPEG q88)"""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    os.makedirs(outdir, exist_ok=True)
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap">'
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': width, 'height': 1400})
        for i, c in enumerate(cards, 1):
            pg.set_content(f'<meta charset="utf-8"><style>{CSS}body{{margin:0;font-family:var(--font)}}.card,.slide{{width:{width}px;border-radius:0!important;box-shadow:none!important}}</style><body>{c}</body>')
            pg.wait_for_timeout(250)
            el = pg.query_selector('.card,.slide')
            png = el.screenshot(type='png')
            im = Image.open(io.BytesIO(png)).convert('RGB')
            if im.size != (1080, 1350): im = im.resize((1080, 1350), Image.LANCZOS)
            im.save(os.path.join(outdir, f'{i:02d}.jpg'), 'JPEG', quality=88, optimize=True)
        b.close()
