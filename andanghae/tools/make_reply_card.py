"""가족방 답장 카드 (정사각, 사이트 파란색).

가족방에 기사가 올라왔을 때 "그래서 우리는 이렇게" 하고 답하는 카드.
사용: python3 make_reply_card.py spec.json 출력폴더  (가로 링크용: 끝에 wide)
spec: {"name": "...", "lead": "공유해 줘서 고마워요", "title": "...", "items": ["...", "...", "..."]}
출력: <name>-reply-1080.jpg (본문·저장용), <name>-reply-800.png (카톡 공유 카드용)
원칙: 하지 말 것은 '~하지 않기'로 끝까지 부정형. 누르는 링크 없음(주소는 그림 글자로만).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

S = 1080
BG = "#1f47b8"
ON = "#ffffff"
ON_SUB = "#d4ddf7"
PILL = "#3c62cc"
CARD = "#ffffff"
INK = "#1d2433"
TEAL = "#2f7d62"
PAD = 84
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-{}.ttc"


def f(size, w="Regular"):
    return ImageFont.truetype(FONT.format(w), size, index=1)


def wrap(d, text, font, maxw):
    out, cur = [], ""
    for ch in text:
        t = cur + ch
        if d.textlength(t, font=font) > maxw and cur:
            sp = cur.rfind(" ")
            if sp > 0 and len(cur) - sp < 9:
                out.append(cur[:sp]); cur = cur[sp + 1:] + ch
            else:
                out.append(cur); cur = ch
        else:
            cur = t
    out.append(cur)
    return [l.strip() for l in out]


def shield(d, x, y, h):
    w = h * 0.86
    pts = [(x, y + h * .14), (x + w / 2, y), (x + w, y + h * .14), (x + w, y + h * .5),
           (x + w / 2, y + h), (x, y + h * .5)]
    d.polygon(pts, fill=ON)
    d.line([(x + w * .27, y + h * .5), (x + w * .45, y + h * .68), (x + w * .76, y + h * .32)],
           fill=BG, width=max(3, int(h * .13)), joint="curve")


def check(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL)
    d.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)],
           fill="white", width=max(3, int(r * .3)), joint="curve")


def make(s, out_dir):
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)
    # 브랜드
    shield(d, PAD, 64, 40)
    d.text((PAD + 48, 86), "순순히안당해", font=f(32, "Bold"), fill=ON, anchor="lm")
    kick = s.get("kick", "가족방 답장 카드")
    kw = d.textlength(kick, font=f(28, "Bold"))
    d.rounded_rectangle([S - PAD - kw - 40, 60, S - PAD, 112], radius=26, fill=PILL)
    d.text((S - PAD - kw - 20, 86), kick, font=f(28, "Bold"), fill=ON, anchor="lm")
    y = 170
    d.text((PAD, y), s.get("lead", "공유해 줘서 고마워요"), font=f(40, "Bold"), fill=ON_SUB)
    y += 70
    for ln in wrap(d, s["title"], f(72, "Black"), S - PAD * 2):
        d.text((PAD, y), ln, font=f(72, "Black"), fill=ON)
        y += 94
    y += 26
    items = s["items"]
    gap = 20
    bottom = S - 130
    box_h = (bottom - y - gap * (len(items) - 1)) / len(items)
    for i, it in enumerate(items):
        top = y + i * (box_h + gap)
        d.rounded_rectangle([PAD, top, S - PAD, top + box_h], radius=24, fill=CARD)
        check(d, PAD + 56, top + box_h / 2, 24)
        tx = PAD + 104
        lines = [l for part in it.split("\n") for l in wrap(d, part, f(40, "Bold"), S - PAD - 30 - tx)]
        th = len(lines) * 54
        ty = top + (box_h - th) / 2
        for ln in lines:
            d.text((tx, ty), ln, font=f(40, "Bold"), fill=INK)
            ty += 54
        if ty > top + box_h + 4:
            print(f"[경고] {i+1}번 칸이 넘칩니다")
    d.line([(PAD, S - 100), (S - PAD, S - 100)], fill=PILL, width=2)
    d.text((PAD, S - 56), "더 알아보려면 주소창에 andanghae.kr 직접 입력", font=f(28), fill=ON_SUB, anchor="lm")
    os.makedirs(out_dir, exist_ok=True)
    p1 = os.path.join(out_dir, f"{s['name']}-reply-1080.jpg")
    img.save(p1, "JPEG", quality=90, optimize=True)
    p2 = os.path.join(out_dir, f"{s['name']}-reply-800.png")
    img.resize((800, 800), Image.LANCZOS).save(p2, "PNG", optimize=True)
    print(p1, os.path.getsize(p1) // 1024, "KB")
    print(p2, os.path.getsize(p2) // 1024, "KB")


if __name__ == "__main__" and len(sys.argv) == 3:
    make(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])


def make_wide(s, out_dir):
    """링크 공유(og:image)용 가로 카드 1200x600 (2:1). 카톡 링크 미리보기에서 잘리지 않게."""
    W, H, P = 1200, 600, 64
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    shield(d, P, 52, 34)
    d.text((P + 42, 70), "순순히안당해", font=f(28, "Bold"), fill=ON, anchor="lm")
    kick = "가족방 답장 카드"
    kw = d.textlength(kick, font=f(24, "Bold"))
    d.rounded_rectangle([W - P - kw - 36, 48, W - P, 92], radius=22, fill=PILL)
    d.text((W - P - kw - 18, 70), kick, font=f(24, "Bold"), fill=ON, anchor="lm")
    # 왼쪽: 인사 + 제목
    lx, lw = P, 430
    y = 150
    d.text((lx, y), s.get("lead", "공유해 줘서 고마워요"), font=f(30, "Bold"), fill=ON_SUB)
    y += 56
    for ln in wrap(d, s["title"], f(56, "Black"), lw):
        d.text((lx, y), ln, font=f(56, "Black"), fill=ON)
        y += 72
    # 오른쪽: 항목
    rx = P + lw + 40
    items = s["items"]
    top0, bottom, gap = 128, H - 96, 14
    box_h = (bottom - top0 - gap * (len(items) - 1)) / len(items)
    for i, it in enumerate(items):
        top = top0 + i * (box_h + gap)
        d.rounded_rectangle([rx, top, W - P, top + box_h], radius=18, fill=CARD)
        check(d, rx + 38, top + box_h / 2, 18)
        tx = rx + 72
        lines = [l for part in it.split("\n") for l in wrap(d, part, f(27, "Bold"), W - P - 20 - tx)]
        ty = top + (box_h - len(lines) * 38) / 2
        for ln in lines:
            d.text((tx, ty), ln, font=f(27, "Bold"), fill=INK)
            ty += 38
        if ty > top + box_h + 4:
            print(f"[경고] 가로 카드 {i+1}번 칸이 넘칩니다")
    d.line([(P, H - 70), (W - P, H - 70)], fill=PILL, width=2)
    d.text((P, H - 38), "더 알아보려면 주소창에 andanghae.kr 직접 입력", font=f(22), fill=ON_SUB, anchor="lm")
    p = os.path.join(out_dir, f"{s['name']}-reply-wide.png")
    img.save(p, "PNG", optimize=True)
    print(p, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] == "wide":
    make_wide(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
