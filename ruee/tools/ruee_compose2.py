"""RUÉE 캐러셀 10장 만들기 v2 (컨셉별 테마).
사용: python3 ruee_compose2.py spec.json OUT_DIR
spec = {"series":"S027","concept":"daily|street|heritage|active","tag":"표지 위 작은 태그","title":["1줄","2줄"],
  "images":[7장: 1 착용표지, 2~6 플랫레이, 7 디테일],
  "notes":[5개: 2~6장 메모], "labels":[5개: 한눈에 보기 짧은 이름],
  "colors":[["이름","#hex"],... 4~5개 팔레트], "tips":["3줄"],
  "accent":"#hex(active 선택)", "sports":[5개 종목 라벨(active 선택)]}
결과: OUT_DIR/S027/01.jpg ~ 10.jpg (1080x1350)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageStat
spec = json.load(open(sys.argv[1])); out = os.path.join(sys.argv[2], spec['series']); os.makedirs(out, exist_ok=True)
FD = os.environ.get('RUEE_FONTS') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts'); NO = '/usr/share/fonts/opentype/noto/'
W, H = 1080, 1350; C = spec['concept']
def cjk(name, s, serif=False): return ImageFont.truetype(NO + ('NotoSerifCJK-' if serif else 'NotoSansCJK-') + name + '.ttc', s, index=1)
def ttf(name, s): return ImageFont.truetype(os.path.join(FD, name), s)
hexrgb = lambda h: tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
THEMES = {
 'daily': dict(name='DAILY', bg='#F3EEE4', ink='#1F1B17', sub='#7A6F63', acc='#B5573A', line='#D6CCBB', title=lambda s: ttf('GowunBatang-Bold.ttf', s), body=lambda s: cjk('Medium', s)),
 'street': dict(name='STREET', bg='#0E0E0E', ink='#F5F5F0', sub='#9A9A94', acc='#C6F432', line='#333333', title=lambda s: ttf('BlackHanSans-Regular.ttf', s), body=lambda s: cjk('Bold', s)),
 'heritage': dict(name='HERITAGE', bg='#14161F', ink='#F1EBDD', sub='#A89F8A', acc='#B89B5E', line='#4A4535', title=lambda s: ttf('SongMyung-Regular.ttf', s), body=lambda s: cjk('Medium', s, True)),
 'active': dict(name='ACTIVE', bg='#F4F4EF', ink='#101114', sub='#6B6E75', acc=spec.get('accent', '#1F4FFF'), line='#D0D2D6', title=lambda s: cjk('Black', s), body=lambda s: cjk('Bold', s)),
}
T = THEMES[C]; BG, INK, SUB, ACC, LINE = [hexrgb(T[k]) for k in ('bg', 'ink', 'sub', 'acc', 'line')]
on_acc = (14, 14, 14) if C in ('street', 'heritage') else (255, 255, 255)
fit = lambda p: Image.open(p).convert('RGB').resize((W, H), Image.LANCZOS)
imgs = [fit(p) for p in spec['images']]
_c = Image.open(spec['images'][0]).convert('RGB'); _w, _h = _c.size
imgs[0] = _c.crop((int(_w * 0.025), int(_h * 0.05), int(_w * 0.975), _h)).resize((W, H), Image.LANCZOS)  # 착용 표지: 턱·입이 보이지 않게 위쪽 5% 잘라냄
TOTAL = 10

def wrap(d, text, font, maxw):
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=font) > maxw and cur:
            cut = cur.rfind(' ')
            if cut > 0: lines.append(cur[:cut]); cur = cur[cut + 1:] + ch
            else: lines.append(cur); cur = ch
        else: cur += ch
    if cur: lines.append(cur)
    return lines

def shear_text(txt, font, fill, k=0.2):
    d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1))); w = int(d0.textlength(txt, font=font)) + 60; h = int(font.size * 1.5)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).text((20, 4), txt, font=font, fill=fill)
    return im.transform((w, h), Image.AFFINE, (1, k, -k * h * 0.5, 0, 1, 0), Image.BICUBIC)

def title_draw(im, lines, x, y, size, fill, step=1.2, skew=False):
    d = ImageDraw.Draw(im)
    for ln in lines:
        if skew and C == 'active':
            t = shear_text(ln, T['title'](size), fill + (255,)) if len(fill) == 3 else shear_text(ln, T['title'](size), fill)
            im.paste(t, (x - 20, y), t)
        else: d.text((x, y), ln, font=T['title'](size), fill=fill)
        y += int(size * step)
    return y

def pill(im, n):  # 하단 중앙: 컨셉 이름 + 장 번호
    d = ImageDraw.Draw(im); t = f"{T['name']}  {n:02d}/{TOTAL}"; f = cjk('Bold', 22); w = d.textlength(t, font=f)
    x = (W - w) / 2 - 22; y = H - 62
    d.rounded_rectangle([x, y, x + w + 44, y + 40], radius=20, fill=ACC if C in ('street', 'active') else (INK if C == 'daily' else BG), outline=ACC if C == 'heritage' else None, width=2)
    d.text((x + 22, y + 6), t, font=f, fill=on_acc if C in ('street', 'active') else (BG if C == 'daily' else ACC))

def busy(im, box):
    sm = im.resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(1))
    diff = ImageChops.difference(sm, sm.filter(ImageFilter.MedianFilter(31))).convert('L').point(lambda v: 255 if v > 28 else 0)
    x0, y0, x1, y1 = [v // 8 for v in box]; return ImageStat.Stat(diff.crop((x0, y0, x1, y1))).mean[0] / 255

def memo(im, text, idx, sport=None, force=None):
    d = ImageDraw.Draw(im); f = T['body'](32); maxw = 330; lines = wrap(d, text, f, maxw)[:3]
    tw = max(d.textlength(l, font=f) for l in lines); bw = int(max(tw, 200) + 60); bh = 70 + 46 * len(lines) + 20; M = 40
    corners = {'tl': (M, M), 'tr': (W - M - bw, M), 'bl': (M, H - M - bh - 40), 'br': (W - M - bw, H - M - bh - 40)}
    x, y = corners[force] if force in corners else min(corners.values(), key=lambda c: busy(im, (c[0], c[1], c[0] + bw, c[1] + bh)))
    card = Image.new('RGBA', (bw + 40, bh + 40), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    sh = Image.new('L', card.size, 0); ImageDraw.Draw(sh).rectangle([26, 28, bw + 26, bh + 28], fill=80); card.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(9)))
    if C == 'daily':
        cd.rectangle([20, 20, bw + 20, bh + 20], fill=(247, 243, 236)); tc, nc = INK, ACC
    elif C == 'street':
        cd.rectangle([20, 20, bw + 20, bh + 20], fill=(12, 12, 12)); cd.rectangle([20, 20, bw + 20, 30], fill=ACC); tc, nc = ACC, (245, 245, 240)
    elif C == 'heritage':
        cd.rectangle([20, 20, bw + 20, bh + 20], fill=(241, 235, 221)); cd.rectangle([28, 28, bw + 12, bh + 12], outline=ACC, width=2); tc, nc = (30, 28, 24), (150, 120, 60)
    else:
        cd.rounded_rectangle([20, 20, bw + 20, bh + 20], radius=26, fill=ACC); tc, nc = (255, 255, 255), (255, 255, 255)
    label = (sport or f'{idx:02d}') if C == 'active' else f'{idx:02d}'
    cd.text((50, 40), label, font=cjk('Black', 22), fill=nc)
    yy = 80
    for l in lines: cd.text((50, yy), l, font=f, fill=tc); yy += 46
    rot = {'street': 2.2, 'daily': 0, 'heritage': 0, 'active': 0}[C]
    if rot: card = card.rotate(rot, resample=Image.BICUBIC, expand=True)
    im.paste(card, (x - 20, y - 20), card); return im

def grad_bottom(base, start=0.52, strength=215, col=(14, 14, 14)):
    g = Image.new('L', (1, H))
    for y in range(H): g.putpixel((0, y), int(strength * max(0, (y - H * start) / (H * (1 - start))) ** 1.15))
    return Image.composite(Image.new('RGB', (W, H), col), base, g.resize((W, H)))

def cover():
    base = imgs[0].copy(); tag = spec['tag']; lines = spec['title'][:2]
    if C == 'daily':
        im = base; d = ImageDraw.Draw(im); ch = 330; y0 = H - ch - 56
        d.rectangle([56, y0, W - 56, y0 + ch], fill=(243, 238, 228))
        d.text((92, y0 + 30), 'RUÉE · DAILY', font=cjk('Bold', 24), fill=ACC); d.text((W - 92 - d.textlength(tag, font=cjk('Medium', 24)), y0 + 30), tag, font=cjk('Medium', 24), fill=SUB)
        d.line([92, y0 + 74, W - 92, y0 + 74], fill=LINE, width=2)
        title_draw(im, lines, 92, y0 + 100, 70, INK, 1.25)
        d.text((92, y0 + ch - 56), '옆으로 넘겨보세요  →', font=cjk('Regular', 26), fill=SUB)
    elif C == 'street':
        im = grad_bottom(base, 0.5, 190); d = ImageDraw.Draw(im)
        y = H - 520
        for ln in lines:
            w = d.textlength(ln, font=T['title'](104)); d.rectangle([60, y, 60 + w + 40, y + 128], fill=ACC); d.text((80, y + 2), ln, font=T['title'](104), fill=(14, 14, 14)); y += 142
        d.text((64, y + 16), tag.upper() if tag.isascii() else tag, font=cjk('Bold', 34), fill=(245, 245, 240))
        st = Image.new('RGBA', (300, 90), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); sd.rounded_rectangle([0, 0, 299, 89], radius=10, fill=ACC); sd.text((24, 14), 'STREET', font=T['title'](56), fill=(14, 14, 14))
        st = st.rotate(8, expand=True, resample=Image.BICUBIC); im.paste(st, (W - 340, 50), st)
        d.text((64, H - 70), '옆으로 넘겨보세요  →', font=cjk('Medium', 28), fill=(220, 220, 214))
    elif C == 'heritage':
        im = grad_bottom(base, 0.5, 210, (14, 16, 24)); d = ImageDraw.Draw(im)
        d.rectangle([34, 34, W - 34, H - 34], outline=ACC, width=3); d.rectangle([48, 48, W - 48, H - 48], outline=ACC, width=1)
        d.text((W / 2 - d.textlength('H E R I T A G E', font=cjk('Medium', 24, True)) / 2, 84), 'H E R I T A G E', font=cjk('Medium', 24, True), fill=ACC)
        y = H - 400
        for ln in lines:
            w = d.textlength(ln, font=T['title'](88)); d.text(((W - w) / 2, y), ln, font=T['title'](88), fill=INK); y += 112
        d.line([W / 2 - 60, y + 14, W / 2 + 60, y + 14], fill=ACC, width=2)
        t = tag; d.text(((W - d.textlength(t, font=cjk('Medium', 28, True))) / 2, y + 36), t, font=cjk('Medium', 28, True), fill=ACC)
    else:
        im = base; blk = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(blk)
        bd.polygon([(0, H - 470), (W, H - 590), (W, H), (0, H)], fill=ACC + (255,)); im.paste(blk, (0, 0), blk)
        bd = ImageDraw.Draw(im); bd.polygon([(0, H - 470), (W, H - 590), (W, H - 574), (0, H - 454)], fill=(255, 255, 255))
        y = title_draw(im, lines, 70, H - 430, 92, (255, 255, 255), 1.15, skew=True)
        d = ImageDraw.Draw(im); tf = cjk('Black', 30); tw = d.textlength(tag, font=tf)
        d.rectangle([70, 60, 70 + tw + 36, 112], fill=(16, 17, 20)); d.text((88, 66), tag, font=tf, fill=(255, 255, 255))
        d.text((70, H - 80), '옆으로 넘겨보세요  →', font=cjk('Bold', 28), fill=(255, 255, 255))
    mf = cjk('Bold', 30, True) if C == 'heritage' else cjk('Black', 30)
    d = ImageDraw.Draw(im); t = 'R U É E'; d.text((W - 70 - d.textlength(t, font=mf), 62 if C != 'active' else 70), t, font=mf, fill=(250, 247, 240) if C != 'active' else (16, 17, 20)) if C not in ('street', 'heritage') else None
    return im

def page():
    im = Image.new('RGB', (W, H), BG); return im, ImageDraw.Draw(im)

def summary():  # 08 한눈에 보기
    im, d = page(); M = 60
    d.text((M, 60), 'R U É E', font=cjk('Bold', 26), fill=ACC); d.text((W - M - d.textlength('ALL LOOKS', font=cjk('Bold', 26)), 60), 'ALL LOOKS', font=cjk('Bold', 26), fill=SUB)
    d.line([M, 112, W - M, 112], fill=LINE, width=2)
    title_draw(im, ['한눈에 보기'], M, 132, 78, INK)
    tw, th = 300, 375; gx = 30; top = 270; labs = spec.get('labels', [''] * 5)
    for i in range(6):
        c, r = i % 3, i // 3; x = M + c * (tw + gx); y = top + r * (th + 96)
        if i < 5:
            th_im = imgs[i + 1].resize((tw, th), Image.LANCZOS); im.paste(th_im, (x, y)); d.rectangle([x, y, x + tw, y + th], outline=LINE, width=2)
            d.rectangle([x, y, x + 52, y + 40], fill=ACC); d.text((x + 10, y + 5), f'{i + 1:02d}', font=cjk('Black', 22), fill=on_acc)
            for k, ln in enumerate(wrap(d, labs[i], T['body'](24), tw)[:2]): d.text((x, y + th + 10 + k * 32), ln, font=T['body'](24), fill=INK)
        else:
            d.rectangle([x, y, x + tw, y + th], outline=LINE, width=2); d.text((x + 20, y + 18), 'COLOR', font=cjk('Black', 22), fill=ACC)
            cols = spec.get('colors', [])[:5]; ch_ = (th - 70) // max(len(cols), 1)
            for k, (nm, hx) in enumerate(cols):
                yy = y + 56 + k * ch_; d.rectangle([x + 20, yy, x + 80, yy + ch_ - 12], fill=hexrgb(hx), outline=LINE); d.text((x + 96, yy + (ch_ - 12) // 2 - 14), nm, font=cjk('Medium', 24), fill=INK)
    pill(im, 8); return im

def tips():  # 09 스타일링 3줄
    im, d = page(); M = 80
    d.text((M, 80), 'R U É E', font=cjk('Bold', 26), fill=ACC)
    d.line([M, 132, W - M, 132], fill=LINE, width=2)
    y = title_draw(im, ['이번 주', '스타일링 3줄'], M, 190, 92, INK, 1.2)
    y += 50
    for k, tp in enumerate(spec['tips'][:3]):
        d.text((M, y), f'{k + 1:02d}', font=cjk('Black', 40), fill=ACC)
        ls = wrap(d, tp, T['body'](38), W - M * 2 - 110)
        for j, ln in enumerate(ls[:3]): d.text((M + 110, y + j * 56), ln, font=T['body'](38), fill=INK)
        y += max(len(ls), 1) * 56 + 56; d.line([M + 110, y - 30, W - M, y - 30], fill=LINE, width=1)
    d.text((M, H - 170), '저장해두고 옷 고를 때 꺼내보세요', font=cjk('Bold', 30), fill=SUB)
    pill(im, 9); return im

def closing():  # 10 마무리
    im = imgs[0].filter(ImageFilter.GaussianBlur(6)); im = Image.blend(im, Image.new('RGB', (W, H), BG), 0.82); d = ImageDraw.Draw(im)
    lines = spec.get('closing', ['내일 뭐 입지 싶을 때', '다시 보러 오세요'])
    y = title_draw(im, lines, 80, 330, 76, INK, 1.3); d = ImageDraw.Draw(im)
    d.text((80, y + 30), '이번 주도 네 가지 컨셉으로 올라와요', font=cjk('Medium', 32), fill=SUB)
    chips = [('MON', 'DAILY', 'daily'), ('WED', 'STREET', 'street'), ('FRI', 'HERITAGE', 'heritage'), ('SAT', 'ACTIVE', 'active')]
    y0 = y + 120; x = 80
    for day, nm, key in chips:
        on = key == C; f = cjk('Black', 28); w = int(d.textlength(f'{day} {nm}', font=f)) + 44
        if x + w > W - 60: x = 80; y0 += 80
        d.rounded_rectangle([x, y0, x + w, y0 + 56], radius=28, fill=ACC if on else None, outline=ACC if not on else None, width=2)
        d.text((x + 22, y0 + 9), f'{day} {nm}', font=f, fill=(on_acc if on else SUB)); x += w + 16
    t = 'R U É E'; mf = cjk('Bold', 34, True); d.text((80, H - 190), t, font=mf, fill=ACC); d.text((80, H - 130), '@ruee_look', font=cjk('Medium', 30), fill=SUB)
    pill(im, 10); return im

cov = cover(); cov.save(f'{out}/01.jpg', quality=88)
notes = spec.get('notes', []); sports = spec.get('sports', [None] * 5); npos = spec.get('note_pos', [None] * 5)
for i in range(5):
    im = imgs[i + 1].copy()
    if i < len(notes) and notes[i].strip(): im = memo(im, notes[i].strip(), i + 1, sports[i] if i < len(sports) else None, npos[i] if i < len(npos) else None)
    pill(im, i + 2); im.save(f'{out}/{i + 2:02d}.jpg', quality=88)
im = imgs[6].copy(); d = ImageDraw.Draw(im); f = cjk('Black', 26); d.rectangle([40, 40, 40 + d.textlength('DETAIL', font=f) + 40, 90], fill=ACC); d.text((60, 48), 'DETAIL', font=f, fill=on_acc)
pill(im, 7); im.save(f'{out}/07.jpg', quality=88)
summary().save(f'{out}/08.jpg', quality=88); tips().save(f'{out}/09.jpg', quality=88); closing().save(f'{out}/10.jpg', quality=88)
print('ok', out)
