"""2026-11-26 채널에 올라가 있는 소식 이미지 47장을 4:3으로 다시 그리기 위한 목록(manifest_43_20261126.json)을 만든다.
내용은 각 소식을 만들 때 쓴 spec 그대로. spec이 없는 10/21 주간 소식과 소개 카드는 올라간 그림에서 옮겨 적음."""
import json
J = lambda p: json.load(open(p, encoding="utf-8"))
out = []
def weekly(tag, s, end_kind):
    date = s["date"]
    out.append(dict(file=f"adh-channel-{tag}-1-43.jpg", kind="cover", page="1/4", date=date, **s["cover"]))
    out.append(dict(file=f"adh-channel-{tag}-2-43.jpg", kind="items", kind_items="news", page="2/4", date=date, **s["news"]))
    out.append(dict(file=f"adh-channel-{tag}-3-43.jpg", kind="items", kind_items="do", page="3/4", date=date, **s["todo"]))
    e = dict(file=f"adh-channel-{tag}-4-43.jpg", kind=end_kind, page="4/4", date=date)
    if tag == "20261014":
        e["band"] = False          # 10/14 카드는 가족방 공유 띠가 생기기 전
    out.append(e)

# 소개(공지 카드) — 16:9 띠 안에만
out.append(dict(file="adh-intro-20261126-43.jpg", kind="intro", kick="소개", lead="처음 오셨나요?",
                title="순순히안당해를 소개해요",
                items=["새 사기·해킹·정보유출이 터지면 쉬운 말로 바로 정리해요",
                       "할 일·하지 않기부터 당했을 때 순서까지 알려 드려요",
                       "가족방에 그대로 보낼 수 있게 카드로 만들어 드려요"]))
for tag in ["20261125", "20261118", "20261111", "20261104", "20261028"]:
    weekly(tag, J(f"spec_channel_{tag}.json"), "end_site")
w1021 = {"date": "10월 21일",
         "cover": {"kicker": "이번 주 사기 소식", "title": "유출이 이어진 한 주,\n다시 모았어요",
                   "sub": "할리스·OK저축은행·새마을금고 유출과 투자 단톡방"},
         "news": {"head": "이번 주 무슨 일이", "items": [
             ["할리스 회원정보 약 276만 건 유출", "지난 소식에서 따로 전했어요"],
             ["OK저축은행 고객 518명 정보 유출", "지난 소식에서 따로 전했어요"],
             ["새마을금고 공제 고객 400여 명 유출", "지난 소식에서 따로 전했어요"],
             ["증권사 사칭 단톡방 투자사기", "지난 소식에서 따로 전했어요"]]},
         "todo": {"head": "이렇게 하세요", "items": [
             ["보상·쿠폰 문자 속 링크는 누르지 않기", "유출 뒤 오는 안내 문자를 조심하세요"],
             ["잔액을 정확히 말해도 끊고 다시 걸기", "앱·통장에 적힌 대표번호로 직접 거세요"],
             ["같은 비밀번호 쓰는 곳부터 바꾸기", "할리스 예전 가입자도 해당될 수 있어요"]]}}
weekly("20261021", w1021, "end_site")
s14 = J("channel_spec_example.json")
s14["cover"] = dict(s14["cover"], title="정보유출이 이어진 한 주,\n알아 둘 5가지")
weekly("20261014", s14, "end_nolink")

# 수법 경보 1장 카드
for tag in ["20261123-kepco", "20261120-flybit", "20261117-kbcapital", "20261113-jumin", "20261110-miraeasset",
            "20261106-phoneloan", "20261103-noshow", "20261030-gifticon", "BITHUMB", "20261028-daishin",
            "20261024-koreanair", "20261020-hollys"]:
    out.append(dict(file=f"adh-alert-{tag}-1-43.jpg", kind="alert", spec=f"spec_alert_{tag}.json"))
# 2장 수법 경보(10/15·10/18): 1번 공유 띠 없는 카드 + 2번 '링크가 없어요'
for tag in ["20261018-ok", "20261015-mg", "20261015"]:
    out.append(dict(file=f"adh-alert-{tag}-1-43.jpg", kind="alert_plain", spec=f"spec_alert_{tag}.json"))
    out.append(dict(file=f"adh-alert-{tag}-2-43.jpg", kind="end_nolink", page="2/2", spec=f"spec_alert_{tag}.json"))

import sys
bith = sys.argv[1] if len(sys.argv) > 1 else "20261029-bithumb"
for c in out:
    if "spec" in c:
        c["spec"] = c["spec"].replace("BITHUMB", bith); c["file"] = c["file"].replace("BITHUMB", bith)
        s = J(c.pop("spec"))
        c["date"] = s["date"]
        if c["kind"].startswith("alert"):
            c.update({k: s["card"][k] for k in ("lead", "kick", "title", "items") if k in s["card"]})
json.dump(out, open("manifest_43_20261126.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "장")
