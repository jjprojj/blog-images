#!/usr/bin/env python3
"""블로그 본문용 간단 인포그래픽 생성기 (800x640 WebP, 보통 20~45KB).
사용: python3 infographic.py spec.json out.webp
spec 예)
{"template":"compare","title":"...","subtitle":"...","blog":"정보두리로","items":[{"head":"개인","rows":["1~10명","..."]}, ...]}
{"template":"steps","title":"...","items":[{"head":"신청","rows":["설명"]}, ...]}      # 3~5단계
{"template":"numbers","title":"...","items":[{"head":"100만원","rows":["만 0세 월 지급액"]}, ...]}  # 2~4개
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont

S = 2                      # 2배로 그린 뒤 축소
W, H = 800 * S, 640 * S      # 5:4 (목록 썸네일 크롭 비율에 맞춤)
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FM = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
KR = 1                     # 'Noto Sans CJK KR' 인덱스는 환경마다 달라 이름으로 찾음
PALETTES = [
    dict(bg="#F5F8FC", main="#1F4E8C", soft="#E3EDF9", text="#1B2430", sub="#5B6B7F"),
    dict(bg="#F4FAF7", main="#1E7A5A", soft="#DDF1E9", text="#14281F", sub="#587064"),
    dict(bg="#FBF7F2", main="#B4531F", soft="#F6E6D8", text="#2B1D12", sub="#7A6554"),
    dict(bg="#F7F6FB", main="#5B3FA6", soft="#E9E3F7", text="#1E1733", sub="#6A6482"),
]

def font(path, size):
    for idx in range(0, 8):
        try:
            f = ImageFont.truetype(path, size, index=idx)
            if "KR" in "".join(f.getname()):
                return f
        except Exception:
            break
    return ImageFont.truetype(path, size)

def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= maxw:
            cur = trial
            continue
        if cur:
            lines.append(cur); cur = ""
        # 단어 자체가 길면 글자 단위로
        for ch in word:
            if draw.textlength(cur + ch, font=f) <= maxw:
                cur += ch
            else:
                lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, xy, text, f, fill, maxw, spacing=1.25):
    x, y = xy
    lines = wrap(draw, text, f, maxw)
    lh = int(f.size * spacing)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y, len(lines)

def fit_rows(draw, rows, maxw, maxh, sizes=(46, 42, 38, 34, 30)):
    for sz in sizes:
        f = font(FM, sz)
        total = 0
        for r in rows:
            total += len(wrap(draw, r, f, maxw)) * int(sz * 1.3) + 14
        if total <= maxh:
            return f
    raise ValueError("텍스트가 칸을 넘칩니다: %r" % rows)

def header(draw, spec, pal):
    ft = font(FB, 60)
    if draw.textlength(spec["title"], font=ft) > W - 160:
        ft = font(FB, 50)
    if draw.textlength(spec["title"], font=ft) > W - 160:
        raise ValueError("제목이 너무 깁니다")
    draw.rectangle([0, 0, 24, H], fill=pal["main"])
    draw.text((80, 56), spec["title"], font=ft, fill=pal["text"])
    if spec.get("subtitle"):
        draw.text((80, 56 + ft.size + 18), spec["subtitle"], font=font(FM, 32), fill=pal["sub"])

def footer(draw, spec, pal):
    fs = font(FM, 26)
    t = spec.get("blog", "")
    if t:
        draw.text((W - 80 - draw.textlength(t, font=fs), H - 60), t, font=fs, fill=pal["sub"])

def render(spec):
    pal = PALETTES[spec.get("palette", 0) % len(PALETTES)]
    img = Image.new("RGB", (W, H), pal["bg"])
    d = ImageDraw.Draw(img)
    header(d, spec, pal)
    items = spec["items"]
    n = len(items)
    top = 270 if spec.get("subtitle") else 230
    bottom = H - 280
    left, right = 80, W - 80
    gap = 36
    cw = (right - left - gap * (n - 1)) // n
    tpl = spec["template"]
    for i, it in enumerate(items):
        x0 = left + i * (cw + gap)
        d.rounded_rectangle([x0, top, x0 + cw, bottom], radius=28, fill="#FFFFFF", outline=pal["soft"], width=4)
        if tpl == "numbers":
            fh = font(FB, 92)
            hw = d.textlength(it["head"], font=fh)
            while hw > cw - 60 and fh.size > 44:
                fh = font(FB, fh.size - 6); hw = d.textlength(it["head"], font=fh)
            d.text((x0 + (cw - hw) / 2, top + 50), it["head"], font=fh, fill=pal["main"])
            rf = fit_rows(d, it["rows"], cw - 60, bottom - top - 220)
            y = top + 190
            for r in it["rows"]:
                y, _ = draw_wrapped(d, (x0 + 30, y), r, rf, pal["text"], cw - 60); y += 14
        else:
            hh = 100
            d.rounded_rectangle([x0, top, x0 + cw, top + hh], radius=28, fill=pal["main"])
            d.rectangle([x0, top + hh - 28, x0 + cw, top + hh], fill=pal["main"])
            head = it["head"]
            if tpl == "steps":
                d.ellipse([x0 + 22, top + 22, x0 + 78, top + 78], fill="#FFFFFF")
                nf = font(FB, 36)
                nt = str(i + 1)
                d.text((x0 + 50 - d.textlength(nt, font=nf) / 2, top + 26), nt, font=nf, fill=pal["main"])
                tx = x0 + 96
            else:
                tx = x0 + 26
            fh = font(FB, 40)
            while d.textlength(head, font=fh) > x0 + cw - 20 - tx and fh.size > 28:
                fh = font(FB, fh.size - 2)
            if d.textlength(head, font=fh) > x0 + cw - 20 - tx:
                raise ValueError("머리글이 칸을 넘칩니다: " + head)
            d.text((tx, top + (hh - fh.size * 1.2) / 2), head, font=fh, fill="#FFFFFF")
            rf = fit_rows(d, it["rows"], cw - 52, bottom - top - hh - 50)
            y = top + hh + 26
            for r in it["rows"]:
                y, _ = draw_wrapped(d, (x0 + 26, y), r, rf, pal["text"], cw - 52); y += 14
    footer(d, spec, pal)
    return img.resize((W // S, H // S), Image.LANCZOS)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    img = render(spec)
    q = 82
    while True:
        img.save(out, "WEBP", quality=q, method=6)
        import os
        if os.path.getsize(out) <= 48000 or q <= 55:
            break
        q -= 6
    print(out, img.size, os.path.getsize(out), "bytes q=%d" % q)
