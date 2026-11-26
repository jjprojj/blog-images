"""순순히안당해 카카오톡 채널 '소식' 카드 4:3 (1200x900 JPG). 2026-11-26

왜: 채널홈은 소식 썸네일을 4:3, 공지 카드를 16:9로 가운데만 잘라 보여 줘서
    1:1(1080) 카드는 위쪽 태그·아래쪽 상자가 잘렸다. 내용·색·글씨체는 그대로 두고 크기와 배치만 바꾼다.
규칙: 1200x900, 글자·상자는 가장자리에서 60px 이상 안쪽.
      공지에 연결하는 소개 카드는 가운데 16:9 띠(세로 112~787, 높이 675) 안에만 내용을 넣는다.

사용: python3 make_channel_cards_43.py manifest.json 출력폴더
manifest: [{"file": "이름.jpg", "kind": "cover|items|end_site|end_nolink|alert|alert_plain|intro", ...}]
"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_channel_cards as m  # 색·글꼴·방패·체크 모양을 그대로 쓴다

W, H = 1200, 900
P = 72                 # 좌우 여백 (60px 이상)
BAND = (112, 787)      # 16:9 가운데 띠 (1200x675)
FOOT_LINE = H - 116    # 아래 구분선
FOOT_Y = H - 80        # 아래 한 줄 (글자 아래 끝이 가장자리에서 60px 이상)
f, wrap = m.f, m.wrap
BG, ON, ON_SUB, PILL, CARD, INK, SUB = m.BG, m.ON, m.ON_SUB, m.PILL, m.CARD, m.INK, m.SUB
YEL, DARK = m.YEL, m.DARK


def header(d, right=None, pill=None, top=64):
    m.shield(d, P, top, 40, ON)
    d.text((P + 48, top + 22), "순순히안당해", font=f(32, "Bold"), fill=ON, anchor="lm")
    if pill:
        kw = d.textlength(pill, font=f(28, "Bold"))
        d.rounded_rectangle([W - P - kw - 40, top - 4, W - P, top + 48], radius=26, fill=PILL)
        d.text((W - P - kw - 20, top + 22), pill, font=f(28, "Bold"), fill=ON, anchor="lm")
    elif right:
        d.text((W - P, top + 22), right, font=f(26), fill=ON_SUB, anchor="rm")


def footer(d, text):
    d.line([(P, FOOT_LINE), (W - P, FOOT_LINE)], fill=PILL, width=2)
    d.text((P, FOOT_Y), text, font=f(24), fill=ON_SUB, anchor="lm")


def new():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def cover(c):
    img, d = new()
    header(d, right=c["page"])
    tf, sf = f(84, "Black"), f(36)
    tl = [l for part in c["title"].split("\n") for l in wrap(d, part, tf, W - P * 2)]
    sl = wrap(d, c["sub"], sf, W - P * 2)
    block = 56 + 34 + len(tl) * 108 + 22 + len(sl) * 54
    y = 130 + (FOOT_LINE - 130 - block) / 2
    kf = f(34, "Bold")
    d.rounded_rectangle([P, y, P + d.textlength(c["kicker"], font=kf) + 44, y + 56], radius=28, fill=PILL)
    d.text((P + 22, y + 28), c["kicker"], font=kf, fill=ON, anchor="lm")
    y += 56 + 34
    for ln in tl:
        d.text((P, y), ln, font=tf, fill=ON)
        y += 108
    y += 22
    for ln in sl:
        d.text((P, y), ln, font=sf, fill=ON_SUB)
        y += 54
    footer(d, f"{c['date']} 소식 · 확인된 사실만 담았어요")
    return img


def items(c):
    img, d = new()
    header(d, right=c["page"])
    d.text((P, 132), c["head"], font=f(56, "Black"), fill=ON)
    y0, y1 = 222, FOOT_LINE - 24
    its = c["items"]
    n = len(its)
    gap = 14
    bh = (y1 - y0 - gap * (n - 1)) / n
    fa, la_h, fb, lb_h = (f(34, "Bold"), 46, f(28), 38) if n <= 4 else (f(32, "Bold"), 42, f(26), 34)
    for i, (a, b) in enumerate(its):
        top = y0 + i * (bh + gap)
        d.rounded_rectangle([P, top, W - P, top + bh], radius=22, fill=CARD)
        if c["kind_items"] == "do":
            m.check(d, P + 52, top + bh / 2, 22)
            tx = P + 96
        else:
            d.text((P + 34, top + bh / 2), str(i + 1), font=f(40, "Black"), fill=BG, anchor="lm")
            tx = P + 90
        maxw = W - P - 30 - tx
        la, lb = wrap(d, a, fa, maxw), wrap(d, b, fb, maxw)
        th = len(la) * la_h + len(lb) * lb_h + 4
        ty = top + (bh - th) / 2 - 2
        for ln in la:
            d.text((tx, ty), ln, font=fa, fill=INK)
            ty += la_h
        ty += 4
        for ln in lb:
            d.text((tx, ty), ln, font=fb, fill=SUB)
            ty += lb_h
        if th > bh - 8:
            print(f"[경고] {c['file']} {i+1}번 칸이 넘칩니다")
    footer(d, f"{c['date']} 소식 · 확인된 사실만 담았어요")
    return img


def share_band(d, y, right):
    m.share_band(d, P, W - P, y, right)


def addr_search(d, y):
    """주소창 상자(왼쪽) · 검색창 상자(오른쪽)를 나란히. 그림 속 글자라 눌리지 않는다."""
    gap = 24
    bw = (W - P * 2 - gap) / 2
    lf = f(30, "Bold")
    d.text((P, y), "주소창에 직접 입력", font=lf, fill=ON)
    d.text((P + bw + gap, y), "또는 검색창에", font=lf, fill=ON)
    y += 48
    d.rounded_rectangle([P, y, P + bw, y + 96], radius=20, fill=CARD)
    d.text((P + 30, y + 48), "andanghae.kr", font=f(46, "Bold"), fill=INK, anchor="lm")
    x0 = P + bw + gap
    d.rounded_rectangle([x0, y, x0 + bw, y + 96], radius=48, fill=CARD)
    cx, cy = x0 + 54, y + 48
    d.ellipse([cx - 18, cy - 18, cx + 14, cy + 14], outline=BG, width=5)
    d.line([(cx + 10, cy + 10), (cx + 26, cy + 26)], fill=BG, width=6)
    d.text((x0 + 98, cy), "순순히안당해", font=f(42, "Bold"), fill=INK, anchor="lm")
    return y + 96


def end_card(c):
    """end_site: '자세한 내용은 순순히안당해에서' (10/20 이후) / end_nolink: '이 소식에는 링크가 없어요' (10/14~10/18)"""
    img, d = new()
    header(d, right=c["page"])
    if c["kind"] == "end_site":
        title = ["자세한 내용은", "순순히안당해에서"]
        sub = ["소식 문구 속 주소를 누르면 글로 바로 가요.", "링크가 걱정되면 직접 찾아오셔도 돼요."]
    else:
        title = ["이 소식에는", "링크가 없어요"]
        sub = ["문자·메시지 속 링크는 누르지 않는 게 기본이에요.", "그래서 저희도 직접 찾아오시게 안내해요."]
    y = 136
    for ln in title:
        d.text((P, y), ln, font=f(66, "Black"), fill=ON)
        y += 84
    y += 8
    for ln in sub:
        d.text((P, y), ln, font=f(30), fill=ON_SUB)
        y += 44
    y = addr_search(d, y + 28)
    if c.get("band", True):
        share_band(d, y + 30, c.get("band_right", "오른쪽 위 공유 버튼"))
        if y + 30 + 76 > FOOT_LINE - 10:
            print("[경고] 끝 카드가 넘칩니다", c["file"])
    footer(d, f"{c['date']} 소식 · 확인된 사실만 담았어요")
    return img


def alert(c):
    """alert: 수법 경보 1장(할 일 3칸 + 공유 띠 + 주소·검색 줄) / alert_plain: 2장 소식의 1번(공유 띠 없이 '더 알아보려면' 줄)"""
    img, d = new()
    header(d, pill=c.get("kick", "채널 소식"))
    d.text((P, 130), c.get("lead", "새 수법 경보"), font=f(36, "Bold"), fill=ON_SUB)
    tf = f(64, "Black")
    tl = wrap(d, c["title"], tf, W - P * 2)
    y = 180
    for ln in tl:
        d.text((P, y), ln, font=tf, fill=ON)
        y += 84
    y += 18
    band = c["kind"] == "alert"
    bottom = (FOOT_LINE - 24 - 76 - 22) if band else (FOOT_LINE - 24)
    its = c["items"]
    gap = 14
    bh = (bottom - y - gap * (len(its) - 1)) / len(its)
    fz, lh = (f(34, "Bold"), 44) if band else (f(36, "Bold"), 48)
    for i, it in enumerate(its):
        top = y + i * (bh + gap)
        d.rounded_rectangle([P, top, W - P, top + bh], radius=22, fill=CARD)
        m.check(d, P + 54, top + bh / 2, 23)
        tx = P + 100
        lines = [l for part in it.split("\n") for l in wrap(d, part, fz, W - P - 30 - tx)]
        ty = top + (bh - len(lines) * lh) / 2 - 2
        for ln in lines:
            d.text((tx, ty), ln, font=fz, fill=INK)
            ty += lh
        if len(lines) * lh > bh - 6:
            print(f"[경고] {c['file']} {i+1}번 칸이 넘칩니다")
    d.line([(P, FOOT_LINE), (W - P, FOOT_LINE)], fill=PILL, width=2)
    if band:
        share_band(d, bottom + 22, f"{c['date']} 소식")
        parts = [("주소창에 ", f(28), ON_SUB), ("andanghae.kr", f(30, "Bold"), ON),
                 ("  ·  검색창에 ", f(28), ON_SUB), ("순순히안당해", f(30, "Bold"), ON)]
    else:
        parts = [("더 알아보려면 주소창에 ", f(28), ON_SUB), ("andanghae.kr", f(30, "Bold"), ON),
                 (" 직접 입력", f(28), ON_SUB)]
    x = P
    for t, fo, col in parts:
        d.text((x, FOOT_Y), t, font=fo, fill=col, anchor="lm")
        x += d.textlength(t, font=fo)
    return img


def intro(c):
    """공지 카드에 연결하는 소개 카드: 모든 내용을 가운데 16:9 띠(112~787) 안에. 띠 위아래는 바탕색만."""
    img, d = new()
    top, bot = BAND
    header(d, pill=c.get("kick", "소개"), top=top + 44)
    y = top + 114
    d.text((P, y), c["lead"], font=f(34, "Bold"), fill=ON_SUB)
    y += 46
    d.text((P, y), c["title"], font=f(60, "Black"), fill=ON)
    y += 88
    its = c["items"]
    rh, gap = 60, 10
    for i, it in enumerate(its):
        t = it.replace("\n", " ")
        d.rounded_rectangle([P, y, W - P, y + rh], radius=18, fill=CARD)
        m.check(d, P + 40, y + rh / 2, 19)
        fz = f(30, "Bold")
        if d.textlength(t, font=fz) > W - P * 2 - 100:
            print("[경고] 소개 항목이 넘칩니다:", t)
        d.text((P + 78, y + rh / 2), t, font=fz, fill=INK, anchor="lm")
        y += rh + gap
    y += 8
    gap2 = 24
    bw = (W - P * 2 - gap2) / 2
    bh = 124
    boxes = [(P, CARD, "자세히 보기", BG, "순순히안당해 사이트", INK),
             (P + bw + gap2, DARK, "알림 받기", YEL, "토스 미니앱 「순순히안당해」", ON)]
    for x, fill, head, hc, name, tc in boxes:
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=22, fill=fill)
        d.text((x + 28, y + 22), head, font=f(32, "Bold"), fill=hc)
        nf = f(34, "Black")
        if d.textlength(name, font=nf) > bw - 56:
            nf = f(30, "Black")
        d.text((x + 28, y + 68), name, font=nf, fill=tc)
    y += bh + 28
    d.text((P, y), "두 곳 링크 모두 이 글 아래에 있어요", font=f(28, "Bold"), fill=YEL, anchor="lm")
    d.text((W - P, y), "가족방 공유: 오른쪽 위 버튼", font=f(26), fill=ON_SUB, anchor="rm")
    if y + 16 > bot - 20:
        print("[경고] 소개 카드가 16:9 띠를 넘습니다", y)
    return img


def end_two(c):
    """사이트·토스 미니앱 상자 2개(같은 크기) 끝 카드. 1080 end_card_new를 4:3에 맞춰 배치만 바꿈.
    공유 띠는 자리가 모자라 아래 한 줄(오른쪽)로 옮긴다."""
    img, d = new()
    header(d, right=c["page"])
    y = 128
    for ln in ["자세한 내용과 알림은", "여기 두 곳에서"]:
        d.text((P, y), ln, font=f(64, "Black"), fill=ON)
        y += 82
    y += 6
    d.text((P, y), "링크가 걱정되면 주소창·검색으로 직접 오셔도 돼요.", font=f(30), fill=ON_SUB)
    y += 60
    m.two_boxes(d, P, y, W - P * 2, 310)
    y += 310 + 18
    d.rounded_rectangle([P, y, W - P, y + 64], radius=32, fill=YEL)
    d.text((W / 2, y + 32), "두 곳 링크 모두 이 글 아래에 있어요", font=f(32, "Bold"), fill=INK, anchor="mm")
    if y + 64 > FOOT_LINE - 12:
        print("[경고] 끝 카드가 넘칩니다", c.get("file"), y + 64)
    d.line([(P, FOOT_LINE), (W - P, FOOT_LINE)], fill=PILL, width=2)
    d.text((P, FOOT_Y), f"{c['date']} 소식 · 확인된 사실만 담았어요", font=f(24), fill=ON_SUB, anchor="lm")
    d.text((W - P, FOOT_Y), "가족방 공유: 오른쪽 위 공유 버튼", font=f(24), fill=ON_SUB, anchor="rm")
    return img


def alert_two(c):
    """수법 경보 1장: 할 일 3칸 + 사이트·토스 미니앱 상자 2개. 1080 alert_single_new를 4:3에 맞춤.
    가로가 넓어져서 할 일은 한 줄로 붙여 쓴다(넘치면 두 줄)."""
    img, d = new()
    header(d, pill=c.get("kick", "채널 소식"))
    d.text((P, 130), c.get("lead", "새 수법 경보"), font=f(36, "Bold"), fill=ON_SUB)
    tf = f(64, "Black")
    tl = wrap(d, c["title"], tf, W - P * 2)
    if len(tl) > 1:
        print("[경고] 제목이 두 줄입니다. 한 줄로 줄이면 칸이 넉넉해요", c.get("file"))
    y = 180
    for ln in tl:
        d.text((P, y), ln, font=tf, fill=ON)
        y += 84
    y += 14
    boxes_h = 200
    band_top = FOOT_LINE - 18 - boxes_h
    its = c["items"]
    gap = 12
    bottom = band_top - 20
    bh = (bottom - y - gap * (len(its) - 1)) / len(its)
    fz, lh = f(34, "Bold"), 44
    for i, it in enumerate(its):
        top = y + i * (bh + gap)
        d.rounded_rectangle([P, top, W - P, top + bh], radius=22, fill=CARD)
        m.check(d, P + 54, top + bh / 2, 23)
        tx = P + 100
        maxw = W - P - 30 - tx
        one = it.replace("\n", " ")
        lines = [one] if d.textlength(one, font=fz) <= maxw else \
            [l for part in it.split("\n") for l in wrap(d, part, fz, maxw)]
        ty = top + (bh - len(lines) * lh) / 2 - 2
        for ln in lines:
            d.text((tx, ty), ln, font=fz, fill=INK)
            ty += lh
        if len(lines) * lh > bh - 6:
            print(f"[경고] {c.get('file')} {i+1}번 칸이 넘칩니다")
    m.two_boxes(d, P, band_top, W - P * 2, boxes_h, compact=True)
    d.line([(P, FOOT_LINE), (W - P, FOOT_LINE)], fill=PILL, width=2)
    d.text((P, FOOT_Y), "두 곳 링크 모두 이 글 아래에 있어요", font=f(28, "Bold"), fill=YEL, anchor="lm")
    d.text((W - P, FOOT_Y), "가족방 공유: 오른쪽 위 버튼", font=f(26), fill=ON_SUB, anchor="rm")
    return img


KINDS = {"cover": cover, "items": items, "end_site": end_card, "end_nolink": end_card,
         "alert": alert, "alert_plain": alert, "intro": intro, "end_two": end_two, "alert_two": alert_two}


def from_spec(spec_path, out_dir):
    """make_channel_cards.py 와 같은 spec.json 으로 4:3 카드를 만든다(새 소식 기본값, 2026-11-26 사용자 규칙).
    토스 링크(channel_links.json)가 있으면 사이트·토스 상자 2개 카드, 없으면 주소창·검색 안내 카드."""
    s = json.load(open(spec_path, encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)
    date, prefix = s["date"], s.get("prefix", "adh-channel")
    two = bool(m.toss_link())
    cards = []
    if s.get("type") == "alert":
        card = dict(s.get("card", {}))
        if not card:
            raise SystemExit("4:3 경보 카드는 spec의 'card'(title·items)가 필요해요. 예전 reply_card 방식은 --square")
        if s.get("cards", 1) == 1:
            cards.append(dict(card, kind="alert_two" if two else "alert", date=date))
        else:
            cards.append(dict(card, kind="alert_plain", date=date))
            cards.append(dict(kind="end_two" if two else "end_nolink", page="2/2", date=date, band=True))
    else:
        cards.append(dict(kind="cover", page="1/4", date=date, **s["cover"]))
        cards.append(dict(kind="items", kind_items="news", page="2/4", date=date, **s["news"]))
        cards.append(dict(kind="items", kind_items="do", page="3/4", date=date, **s["todo"]))
        cards.append(dict(kind="end_two" if two else "end_site", page="4/4", date=date))
    paths = []
    for i, c in enumerate(cards, 1):
        c["file"] = f"{prefix}-{i}.jpg"
        im = KINDS[c["kind"]](c)
        p = os.path.join(out_dir, c["file"])
        im.save(p, "JPEG", quality=90, optimize=True)
        print(p, im.size, os.path.getsize(p) // 1024, "KB")
        paths.append(p)
    return paths


def main(manifest, out_dir):
    cards = json.load(open(manifest, encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)
    for c in cards:
        im = KINDS[c["kind"]](c)
        p = os.path.join(out_dir, c["file"])
        im.save(p, "JPEG", quality=90, optimize=True)
        print(p, im.size, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
