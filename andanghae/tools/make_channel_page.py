"""채널 카드 소식 확인 페이지(운영자용) 만들기.

사용: python3 make_channel_page.py spec.json 출력폴더
spec.json 의 prefix, date, post.title, post.body 를 읽어
출력폴더/<prefix>.html 과 <prefix>-body.txt(완성된 소식 문구) 를 만든다.
2026-11-26: post.body 에는 요약과 ▪ 할 일까지만 쓴다. 끝부분(🔍 사이트 · 🔔 토스 미니앱 안내, 검색 안내, 가족방 공유)은
이 도구가 붙인다. post.site_desc(사이트 묶음 한 줄 설명), post.link(글 1개) 또는 post.links([[제목, 주소], …] 주간 소식)를 쓴다.
토스 링크는 channel_links.json 의 "toss"; 비어 있으면 예전 끝부분(사이트 주소·검색 안내·공유)으로 만든다.
2026-11-27: 사이트 안내 이모지를 📖 → 🔍 로 바꿈(흰 책이 폰에서 잘 안 보임). 개별 소식 순서는 사이트(자세히 보기) → 토스(알림 받기) 그대로.
예전 형식(body 안에 '가족방에도 공유해 주세요'까지 들어 있음)은 그대로 쓴다. 같은 폴더에 <prefix>-1~4.jpg 가 있어야 한다.
페이지 주소: https://jjprojj.github.io/blog-images/andanghae/channel/<prefix>.html
카드마다 [저장] 버튼, 제목·문구마다 [복사] 버튼.
"""
import html
import json
import os
import sys

TPL = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>채널 카드 소식 {date}</title>
<style>
:root{{--blue:#1f47b8;--ink:#1d2433;--sub:#5a6274;--line:#e4e7ed;--bg:#f4f6fb}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,"Noto Sans KR","Apple SD Gothic Neo",sans-serif;line-height:1.6}}
header{{background:var(--blue);color:#fff;padding:18px 16px 20px}}
header small{{opacity:.85}}
header h1{{margin:4px 0 0;font-size:22px}}
main{{max-width:560px;margin:0 auto;padding:16px}}
.box{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px;margin-bottom:14px}}
.steps{{font-size:15px;margin:0;padding-left:20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}}
.card img{{width:100%;border-radius:10px;display:block;border:1px solid var(--line)}}
.btn{{display:block;width:100%;margin-top:6px;padding:11px 0;border:0;border-radius:10px;background:var(--blue);color:#fff;font-size:15px;font-weight:700;text-align:center;text-decoration:none;cursor:pointer}}
.btn.light{{background:#e8edfa;color:var(--blue)}}
h2{{font-size:16px;margin:0 0 8px}}
.txt{{white-space:pre-wrap;background:#f8f6f1;border-radius:10px;padding:12px;font-size:15px}}
.done{{background:#2f7d62!important;color:#fff!important}}
.note{{font-size:13px;color:var(--sub)}}
</style></head><body>
<header><small>순순히안당해 채널 카드 소식 · {date}</small><h1>{title}</h1></header>
<main>
<div class="box"><ol class="steps">
<li>카드 {n}장 [저장] 누르기{all_hint}</li>
<li>카카오톡 채널 관리자 앱 → 소식 → 새 소식 작성</li>
<li>사진 {n}장을 넣고, 제목·문구 [복사] → 붙여 넣기 (문구 안에 링크가 다 들어 있어요)</li>
<li>{step4}</li></ol></div>
<div class="grid">{cards}</div>
{save_all}
<div class="box"><h2>제목</h2><div class="txt" id="t">{title}</div>
<button class="btn" onclick="cp('t',this)">제목 복사</button></div>
<div class="box"><h2>문구</h2><div class="txt" id="b">{body}</div>
<button class="btn" onclick="cp('b',this)">문구 복사</button></div>
{linkbox}
<p class="note">이 화면은 운영자 확인용이에요(검색에 나오지 않아요). 고칠 곳이 있으면 Claude 대화창에 "이번 주 카드 2장째 이렇게 바꿔줘"처럼 말하면 돼요. 올리지 않아도 괜찮아요.</p>
</main>
<script>
function cp(id,btn){{var s=document.getElementById(id).innerText;
 var ok=function(){{var o=btn.textContent;btn.textContent='복사됐어요';btn.classList.add('done');setTimeout(function(){{btn.textContent=o;btn.classList.remove('done')}},1800)}};
 if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(s).then(ok,function(){{fb(s);ok()}})}}else{{fb(s);ok()}}}}
function fb(s){{var a=document.createElement('textarea');a.value=s;document.body.appendChild(a);a.select();try{{document.execCommand('copy')}}catch(e){{}}a.remove()}}
// 4장 모두 저장: 1→2→3→4 순서를 지키려고 그림을 미리 모두 받아 둔 뒤, 한 장씩 저장하고 다음 장 전에 충분히 기다린다.
// (예전처럼 0.7초 간격으로 한꺼번에 누르면 휴대폰이 받는 순서가 뒤섞여 2,1,3,4로 저장되는 일이 있었다)
function wait(ms){{return new Promise(function(r){{setTimeout(r,ms)}})}}
async function saveAll(){{var btn=document.getElementById('saveall');if(btn.disabled)return;var o=btn.textContent;btn.disabled=true;
 var l=Array.prototype.slice.call(document.querySelectorAll('a[download]'));var urls=[];
 try{{btn.textContent='준비 중…';for(var i=0;i<l.length;i++){{var r=await fetch(l[i].getAttribute('href'),{{cache:'no-store'}});urls.push(URL.createObjectURL(await r.blob()))}}}}catch(e){{urls=null}}
 for(var j=0;j<l.length;j++){{btn.textContent=(j+1)+'번 저장 중 ('+(j+1)+'/'+l.length+')';
  var a=document.createElement('a');a.href=urls?urls[j]:l[j].getAttribute('href');a.download=l[j].getAttribute('download');document.body.appendChild(a);a.click();a.remove();
  await wait(j===0?2500:1800)}}
 if(urls)urls.forEach(function(u){{URL.revokeObjectURL(u)}});
 btn.textContent='다 저장했어요 (1→2→3→4)';setTimeout(function(){{btn.textContent=o;btn.disabled=false}},2500)}}
</script></body></html>"""

CARD = '<div class="card"><img src="{f}" alt="카드 {i}"><a class="btn" href="{f}" download="{f}">{i}번 저장</a></div>'


TAIL_DEFAULT_DESC = "어떤 수법인지, 당했을 때 할 일까지 정리했어요."
SHARE = "가족방에도 공유해 주세요. 소식 화면 오른쪽 위 공유 버튼을 누르면 카톡 대화방으로 바로 보낼 수 있어요."


def toss_link():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "channel_links.json")
    try:
        return (json.load(open(p, encoding="utf-8")).get("toss") or "").strip()
    except Exception:
        return ""


def compose(post, toss):
    """요약·할 일 뒤에 사이트·토스 안내를 붙여 완성된 소식 문구를 만든다."""
    body = post["body"].rstrip()
    if "가족방에도 공유해 주세요" in body:      # 예전 형식: 이미 끝부분까지 들어 있음
        return body
    links = post.get("links") or ([["", post["link"]]] if post.get("link") else [])
    if toss:
        site = ["🔍 자세히 보기 · 순순히안당해 사이트 (휴대폰·PC 모두)", post.get("site_desc") or TAIL_DEFAULT_DESC]
        for label, url in links:
            if label:
                site.append("· " + label)
            site.append("👉 " + url)
        site.append("주소를 누르기 망설여지면 주소창에 andanghae.kr, 검색창에 '순순히안당해'를 쳐서 들어와도 돼요.")
        app = ["🔔 알림 받기 · 토스 미니앱 「순순히안당해」",
               "앱 설치 없이 토스에서 바로 열려요. 새 사기 수법이나 개인정보 유출이 나오면 바로 알려 드려요.",
               "👉 " + toss]
        return "\n\n".join([body, "\n".join(site), "\n".join(app), SHARE])
    site = ["자세히 보기"]
    for label, url in links:
        if label:
            site.append("· " + label)
        site.append(url)
    return "\n\n".join([body, "\n".join(site),
                         "주소를 누르기 망설여지면 검색창에 '순순히안당해'를 쳐서 들어와도 돼요.", SHARE])


def main(spec_path, out_dir):
    s = json.load(open(spec_path, encoding="utf-8"))
    p = s["prefix"]
    n = s.get("cards", 1) if s.get("type") == "alert" else 4
    cards = "".join(CARD.format(f=f"{p}-{i}.jpg", i=i) for i in range(1, n + 1))
    for i in range(1, n + 1):
        if not os.path.exists(os.path.join(out_dir, f"{p}-{i}.jpg")):
            sys.exit(f"카드 {i}번 파일이 없습니다")
    toss = toss_link()
    body = compose(s["post"], toss)
    link = s["post"].get("link") or (s["post"].get("links") or [["", ""]])[0][1]
    # 우리 사이트 글 주소와 우리 토스 미니앱 링크만 허용
    import re
    urls = re.findall(r"https?://\S+", body)
    if link and not link.startswith("https://andanghae.kr/"):
        sys.exit("링크는 andanghae.kr 글 주소만 넣을 수 있습니다")
    bad = [u for u in urls if not (u == "https://andanghae.kr" or u.startswith("https://andanghae.kr/") or (toss and u == toss))]
    if bad:
        sys.exit("문구에 andanghae.kr·토스 미니앱 말고 다른 주소가 들어 있습니다: " + ", ".join(bad))
    # 2026-10-20: 카카오 소식 작성 화면에 '링크 추가' 칸이 없어 문구만 붙여 넣는다(주소는 문구 안에)
    # 2026-11-26: 소식 버튼을 달 수 있으면 사이트('자세히 보기')로, 하나 더 달 수 있으면 토스 링크
    step4 = "게시 (소식 버튼을 달 수 있으면 아래 '(선택) 소식 버튼용'에서 사이트 링크 복사)"
    btns = []
    if link:
        btns.append(('ls', '자세히 보기 · 사이트 링크', link))
    if toss:
        btns.append(('lt', '알림 받기 · 토스 미니앱 링크 (버튼 하나 더 달 수 있을 때)', toss))
    linkbox = ""
    if btns:
        rows = "".join(f'<p class="note" style="margin:8px 0 2px">{html.escape(t)}</p><div class="txt" id="{i}">{html.escape(u)}</div>'
                       f'<button class="btn light" onclick="cp(\'{i}\',this)">복사</button>' for i, t, u in btns)
        linkbox = f'<div class="box"><h2>(선택) 소식 버튼용</h2><p class="note" style="margin:0">문구에 이미 두 링크가 다 들어 있어요. 버튼을 달 때만 쓰세요.</p>{rows}</div>'
    page = TPL.format(date=html.escape(s["date"]), title=html.escape(s["post"]["title"]),
                      body=html.escape(body), cards=cards, n=n, step4=step4, linkbox=linkbox,
                      all_hint=f" (또는 맨 아래 [{n}장 모두 저장])" if n > 1 else "",
                      save_all=f'<button id="saveall" class="btn light" style="margin:-4px 0 14px" onclick="saveAll()">{n}장 모두 저장</button>' if n > 1 else "")
    out = os.path.join(out_dir, f"{p}.html")
    open(out, "w", encoding="utf-8").write(page)
    open(os.path.join(out_dir, f"{p}-body.txt"), "w", encoding="utf-8").write(body)
    print(out)
    print(os.path.join(out_dir, f"{p}-body.txt"))
    print(f"https://jjprojj.github.io/blog-images/andanghae/channel/{p}.html")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
