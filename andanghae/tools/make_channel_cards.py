"""순순히안당해 카카오톡 채널 '소식' 카드 4장 (1080x1080 JPG).

사용: python3 make_channel_cards.py spec.json 출력폴더
수법 경보 단독 소식: spec에 "type": "alert" + "card"(답장 카드 형식 title/items, lead·kick 바꿈) 또는 "reply_card"(기존 jpg 경로) → 2장(요약 카드 + 링크 없음 안내)
spec.json 예시는 같은 폴더의 channel_spec_example.json.
카드: 1 표지 / 2 이번 주 무슨 일이 / 3 이렇게 하세요 / 4 링크 없음 안내(고정)
원칙: 주소·링크를 넣지 않는다. 하지 말 것은 끝까지 부정형으로 쓴다. 빨간 경고색은 쓰지 않는다.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1080
BG = "#1f47b8"   # 사이트 파란색
ON = "#ffffff"   # 파란 바탕 위 글자
ON_SUB = "#d4ddf7"
PILL = "#3c62cc"
CARD = "#ffffff"
NAVY = "#1f3a68"
INK = "#1d2433"
SUB = "#5a6274"
TEAL = "#2f7d62"
TEAL_BG = "#e8f2ed"
LINE = "#e4e7ed"
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


def shield(d, x, y, h, color):
    w = h * 0.86
    pts = [(x, y + h * .14), (x + w / 2, y), (x + w, y + h * .14), (x + w, y + h * .5),
           (x + w / 2, y + h), (x, y + h * .5)]
    d.polygon(pts, fill=color)
    d.line([(x + w * .27, y + h * .5), (x + w * .45, y + h * .68), (x + w * .76, y + h * .32)],
           fill=BG if color == ON else "white", width=max(3, int(h * .13)), joint="curve")


def check(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL)
    d.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)],
           fill="white", width=max(3, int(r * .3)), joint="curve")


def base(page, date, total=4):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # 브랜드 줄
    y = 64
    shield(d, PAD, y, 40, ON)
    d.text((PAD + 48, y + 22), "순순히안당해", font=f(32, "Bold"), fill=ON, anchor="lm")
    d.text((W - PAD, y + 22), f"{page}/{total}", font=f(26), fill=ON_SUB, anchor="rm")
    # 아래 띠
    d.line([(PAD, H - 92), (W - PAD, H - 92)], fill=PILL, width=2)
    d.text((PAD, H - 50), f"{date} 소식 · 확인된 사실만 담았어요", font=f(24), fill=ON_SUB, anchor="lm")
    return img, d


def cover(s, date):
    img, d = base(1, date)
    c = s["cover"]
    tl = wrap(d, c["title"], f(86, "Black"), W - PAD * 2)
    sl = wrap(d, c["sub"], f(38), W - PAD * 2)
    block = 80 + len(tl) * 112 + 30 + len(sl) * 58
    y = 130 + (H - 92 - 130 - block) / 2 - 20
    d.rounded_rectangle([PAD, y, PAD + d.textlength(c["kicker"], font=f(36, "Bold")) + 44, y + 58],
                        radius=29, fill=PILL)
    d.text((PAD + 22, y + 29), c["kicker"], font=f(36, "Bold"), fill=ON, anchor="lm")
    y += 92
    for ln in tl:
        d.text((PAD, y), ln, font=f(86, "Black"), fill=ON)
        y += 112
    y += 30
    for ln in sl:
        d.text((PAD, y), ln, font=f(38), fill=ON_SUB)
        y += 58
    return img


def items_card(page, head, items, date, kind):
    img, d = base(page, date)
    y = 170
    d.text((PAD, y), head, font=f(60, "Black"), fill=ON)
    y += 112
    n = len(items)
    gap = 18
    box_h = (H - 130 - y - gap * (n - 1)) / n
    for i, (a, b) in enumerate(items):
        top = y + i * (box_h + gap)
        d.rounded_rectangle([PAD, top, W - PAD, top + box_h], radius=22,
                            fill=CARD)
        tx = PAD + 34
        if kind == "do":
            check(d, PAD + 52, top + box_h / 2, 22)
            tx = PAD + 96
        else:
            d.text((PAD + 34, top + box_h / 2), str(i + 1), font=f(40, "Black"), fill=BG, anchor="lm")
            tx = PAD + 90
        maxw = W - PAD - 30 - tx
        fa = f(36, "Bold")
        fb = f(29)
        la = wrap(d, a, fa, maxw)
        lb = wrap(d, b, fb, maxw)
        th = len(la) * 48 + len(lb) * 40 + 6
        ty = top + (box_h - th) / 2
        for ln in la:
            d.text((tx, ty), ln, font=fa, fill=INK)
            ty += 48
        ty += 6
        for ln in lb:
            d.text((tx, ty), ln, font=fb, fill=SUB)
            ty += 40
        if ty > top + box_h + 4:
            print(f"[경고] {page}번 카드 {i+1}번 칸이 넘칩니다")
    return img


def end_card(date, page=4, total=4):
    img, d = base(page, date, total)
    y = 150
    for ln in ["이 소식에는", "링크가 없어요"]:
        d.text((PAD, y), ln, font=f(74, "Black"), fill=ON)
        y += 94
    y += 14
    for ln in ["문자·메시지 속 링크는 누르지 않는 게 기본이에요.", "그래서 저희도 직접 찾아오시게 안내해요."]:
        d.text((PAD, y), ln, font=f(33), fill=ON_SUB)
        y += 48
    y += 26
    # 1) 주소창에 직접 입력 (그림 속 글자라 눌리지 않음)
    d.text((PAD, y), "주소창에 직접 입력", font=f(32, "Bold"), fill=ON)
    y += 52
    d.rounded_rectangle([PAD, y, W - PAD, y + 104], radius=20, fill=CARD)
    d.text((PAD + 34, y + 52), "andanghae.kr", font=f(50, "Bold"), fill=INK, anchor="lm")
    y += 124
    # 2) 또는 검색
    d.text((PAD, y), "또는 검색창에", font=f(32, "Bold"), fill=ON)
    y += 52
    d.rounded_rectangle([PAD, y, W - PAD, y + 104], radius=52, fill=CARD)
    cx, cy = PAD + 58, y + 52
    d.ellipse([cx - 18, cy - 18, cx + 14, cy + 14], outline=BG, width=5)
    d.line([(cx + 10, cy + 10), (cx + 26, cy + 26)], fill=BG, width=6)
    d.text((PAD + 104, cy), "순순히안당해", font=f(44, "Bold"), fill=INK, anchor="lm")
    y += 104 + 30
    # 3) 가족방 공유 안내 (카카오 소식 아래 공유 버튼을 쓰게 안내)
    d.rounded_rectangle([PAD, y, W - PAD, y + 76], radius=38, fill=PILL)
    sx, sy = PAD + 46, y + 38          # 공유 모양(점 3개 연결)
    pts = [(sx - 14, sy), (sx + 12, sy - 15), (sx + 12, sy + 15)]
    d.line([pts[1], pts[0], pts[2]], fill=ON, width=4)
    for (px, py) in pts:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=ON)
    d.text((PAD + 84, sy), "가족방에도 공유해 주세요", font=f(32, "Bold"), fill=ON, anchor="lm")
    d.text((W - PAD - 30, sy), "소식 아래 공유 버튼", font=f(26), fill=ON_SUB, anchor="rm")
    if y + 76 > H - 100:
        print("[경고] 마지막 카드가 넘칩니다")
    return img


def main(spec_path, out_dir):
    s = json.load(open(spec_path, encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)
    date = s["date"]
    prefix = s.get("prefix", "adh-channel")
    if s.get("type") == "alert":
        # 수법 경보 단독 소식: 1번 = 이미 만든 가족방 답장 카드, 2번 = 링크 없음 안내
        if "card" in s:   # 답장 카드 틀로 채널용 1번 카드를 새로 그림(머리말·꼬리표만 채널용)
            import tempfile
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import make_reply_card as rc
            c = dict(s["card"]); c.setdefault("name", prefix)
            tmp = tempfile.mkdtemp()
            rc.make(c, tmp)
            src = os.path.join(tmp, f"{c['name']}-reply-1080.jpg")
        else:
            src = os.path.join(os.path.dirname(os.path.abspath(spec_path)), s["reply_card"]) \
                if not os.path.isabs(s["reply_card"]) else s["reply_card"]
        first = Image.open(src).convert("RGB").resize((W, H))
        cards = [first, end_card(date, 2, 2)]
        for i, im in enumerate(cards, 1):
            p = os.path.join(out_dir, f"{prefix}-{i}.jpg")
            im.save(p, "JPEG", quality=88, optimize=True)
            print(p, os.path.getsize(p) // 1024, "KB")
        return
    cards = [
        cover(s, date),
        items_card(2, s["news"]["head"], s["news"]["items"], date, "news"),
        items_card(3, s["todo"]["head"], s["todo"]["items"], date, "do"),
        end_card(date),
    ]
    for i, im in enumerate(cards, 1):
        p = os.path.join(out_dir, f"{prefix}-{i}.jpg")
        im.save(p, "JPEG", quality=88, optimize=True)
        print(p, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
