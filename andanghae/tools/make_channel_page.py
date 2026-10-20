"""채널 카드 소식 확인 페이지(운영자용) 만들기.

사용: python3 make_channel_page.py spec.json 출력폴더
spec.json 의 prefix, date, post.title, post.body 를 읽어
출력폴더/<prefix>.html 을 만든다. 같은 폴더에 <prefix>-1~4.jpg 가 있어야 한다.
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
<li>사진 {n}장을 넣고, 제목·문구 [복사] → 붙여 넣기</li>
<li>'링크 추가'는 쓰지 않고 게시</li></ol></div>
<div class="grid">{cards}</div>
{save_all}
<div class="box"><h2>제목</h2><div class="txt" id="t">{title}</div>
<button class="btn" onclick="cp('t',this)">제목 복사</button></div>
<div class="box"><h2>문구</h2><div class="txt" id="b">{body}</div>
<button class="btn" onclick="cp('b',this)">문구 복사</button></div>
<p class="note">이 화면은 운영자 확인용이에요(검색에 나오지 않아요). 고칠 곳이 있으면 Claude 대화창에 "이번 주 카드 2장째 이렇게 바꿔줘"처럼 말하면 돼요. 올리지 않아도 괜찮아요.</p>
</main>
<script>
function cp(id,btn){{var s=document.getElementById(id).innerText;
 var ok=function(){{var o=btn.textContent;btn.textContent='복사됐어요';btn.classList.add('done');setTimeout(function(){{btn.textContent=o;btn.classList.remove('done')}},1800)}};
 if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(s).then(ok,function(){{fb(s);ok()}})}}else{{fb(s);ok()}}}}
function fb(s){{var a=document.createElement('textarea');a.value=s;document.body.appendChild(a);a.select();try{{document.execCommand('copy')}}catch(e){{}}a.remove()}}
function saveAll(){{var l=document.querySelectorAll('a[download]');l.forEach(function(a,i){{setTimeout(function(){{a.click()}},i*700)}})}}
</script></body></html>"""

CARD = '<div class="card"><img src="{f}" alt="카드 {i}"><a class="btn" href="{f}" download="{f}">{i}번 저장</a></div>'


def main(spec_path, out_dir):
    s = json.load(open(spec_path, encoding="utf-8"))
    p = s["prefix"]
    n = s.get("cards", 1) if s.get("type") == "alert" else 4
    cards = "".join(CARD.format(f=f"{p}-{i}.jpg", i=i) for i in range(1, n + 1))
    for i in range(1, n + 1):
        if not os.path.exists(os.path.join(out_dir, f"{p}-{i}.jpg")):
            sys.exit(f"카드 {i}번 파일이 없습니다")
    body = s["post"]["body"]
    if "http" in body or "andanghae.kr" in body:
        sys.exit("문구에 주소가 들어 있습니다")
    page = TPL.format(date=html.escape(s["date"]), title=html.escape(s["post"]["title"]),
                      body=html.escape(body), cards=cards, n=n,
                      all_hint=f" (또는 맨 아래 [{n}장 모두 저장])" if n > 1 else "",
                      save_all=f'<button class="btn light" style="margin:-4px 0 14px" onclick="saveAll()">{n}장 모두 저장</button>' if n > 1 else "")
    out = os.path.join(out_dir, f"{p}.html")
    open(out, "w", encoding="utf-8").write(page)
    print(out)
    print(f"https://jjprojj.github.io/blog-images/andanghae/channel/{p}.html")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
