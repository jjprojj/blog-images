# 카쌉 인스타 주간 작업 지시서 (일요일 예약 작업이 읽는다)

모든 답과 메일은 한국어, 쉬운 말, 줄표(—) 쓰지 않기.

## 고정 값
- 시트 `카쌉_인스타_대기열` id `1Q5dcBDow5MT0yc2sktxeYUP5qag72riCt9cpfYh_44M`
  - 탭 `게시` 열: A번호 B상태 C게시예정(KST 'yyyy-MM-dd HH:mm' 글자) D유형 E제목 F장수 G캡션 H이미지폴더 I게시ID J결과·메모 K코드
  - 탭 `설정` 열: A키 B값 (키 `검수페이지URL`에 검수 페이지 주소를 적어 둔다)
- 카드 저장소 `jjprojj/blog-images` 폴더 `carssap/<번호>/01.jpg ... 05.jpg` (공개 주소 https://jjprojj.github.io/blog-images/carssap/<번호>/01.jpg). 이 저장소의 `carssap/_src/`가 이 도구 모음이다.
- 배경 사진 풀: `carssap/photos/NNN.jpg` (가로 1080 이상) + `carssap/_src/photos.json` (번호 → {tags, used:[글번호]}). 같은 사진은 8주 안에 다시 쓰지 않는다. 사진에는 글자가 없어야 한다.
- 차량 데이터: https://carssap.com/wp-content/plugins/chabigyo/data/cars.json (막히면 `cars_snapshot.json`). 키: cars[] {id,brand,name,body,segment,length,width,height,wheelbase,seats,trunk,powertrains[{label,fuel,efficiency,range_km,price_from_krw,price_note}]}. 크기는 mm.

## 주간 구성 (게시는 매일 10:00 KST)
월 실용 · 화 크기 비교 · 수 순위 · 목 실용 · 토 크기 비교. 글 1개 = 카드 5장.
작업 시작 시점의 다음 월요일부터 그 주 토요일까지를 만든다(첫 회차는 지시를 따른다). 번호는 시트 `게시` 탭의 마지막 번호 다음부터 1씩 올린다.

## 단계
1. 준비: `git clone --depth 1 --filter=blob:none --sparse https://github.com/jjprojj/blog-images.git` 후 `git sparse-checkout set carssap`. `pip install playwright pillow`가 필요하면 설치(크로뮴은 이미 있음). `sys.path`에 `carssap/_src`를 넣고 `import cards, art, review_page`.
2. 기록 읽기: 시트 `게시` 탭 전체와 `photos.json`을 읽어 이미 다룬 주제·차종·사진을 피한다. 반려된 글의 J열 이유가 있으면 이번 주 작성에 반영한다.
3. 주제 정하기
   - 크기 비교(화·토): 독자가 실제로 고민하는 두 차(같은 가격대, 세단 대 SUV, 전기차 대 내연기관 등). 길이·높이·휠베이스·시작가·연간 연료비 차이를 데이터로 계산한다. 연료비는 연 15,000km, 공인 연비·전비 기준이고 전기요금·유가 가정은 카드에 적는다.
   - 순위(수): 데이터로 계산 가능한 숫자 순위(예: 1㎡당 시작가, 트렁크 용량, 연비). TOP 3~5, 기준을 카드에 분명히 적는다.
   - 실용(월·목): 현실에서 실제로 많이 생기는 일(차키 배터리, 방전·점프, 겨울 시동, 타이어 공기압, 사고 났을 때 순서, 블랙박스, 워셔액·성에 등)을 웹 검색으로 조사해 정확히 쓴다. 차종마다 다른 내용은 "차종마다 달라요, 사용설명서 확인"을 넣는다. 안전과 관련된 내용은 공식 자료(제조사, 도로교통공단, 소방청 등)로 확인한다.
4. 카드 만들기 (모두 1080x1350 JPEG, `cards.render(html_list, 폴더)`)
   - 크기 비교와 순위 숫자 카드: `reference_build_week.py`의 패턴(`overlay`, `stack`, `roofs`, `bars`, `rowsvg`, `cards.slide('cmp'|'rank', ...)`). 크기 비교는 사이트 차 윤곽(`art.car`)을 얇은 선으로, 글자는 크게.
   - 실용 카드: 사진 카드. 1장 `cards.photo_cover`, 중간 `cards.photo_steps`(단계 목록), 마지막 `cards.photo_big`+CTA. 순위 표지는 `cards.photo_rank_cover`를 쓸 수 있다.
   - 5장 구성: 1 표지 → 2~4 핵심 → 5 마무리(프로필 링크 · 카쌉에서 확인).
   - 만든 뒤 반드시 이미지를 직접 열어 글자 잘림, 겹침, 읽기 어려움, 숫자 오류를 확인하고 고친다. 사진 위 글씨가 안 읽히면 사진을 바꾼다.
5. 캡션 (G열, 모바일 가독성): 첫 문장은 두 줄로 나눈다. ▪ 항목마다 빈 줄. 날짜·수치는 "▪ 항목" 아래 "· 세부" 한 줄씩. 긴 설명은 문장마다 줄바꿈. 마지막에 "프로필 링크에서 카쌉 보기" 한 줄과 해시태그 5개 이하.
6. 올리기: 카드를 `carssap/<번호>/NN.jpg`로 저장소에 git push(github API 쓰기는 막혀 있고 git push는 된다). 이전에 `게시완료`된 글의 `carssap/<번호>/` 폴더는 지운다. `photos.json`에 사용 기록을 남기고 같이 push.
7. 시트 기록: `게시` 탭 끝에 글마다 한 줄 추가(상태 `검수대기`, 게시예정 'yyyy-MM-dd 10:00', 장수 5, 이미지폴더=번호). 값은 글자로 쓴다.
8. 검수 페이지: 카드 5장을 가로 720(720x900)으로 줄여 JPEG 품질 74 데이터 주소로 넣고 `review_page.build(posts, 시트id, '월/일~월/일')`로 HTML을 만든다. Artifact 도구로 게시한다. 처음은 새로 만들고(`capabilities: {"mcp": {"servers": [{"server": "Google Sheets", "tools": ["get_values", "update_values"]}]}}`, 첫 게시 때 title '카쌉 주간 검수'), 주소를 설정 탭 `검수페이지URL`에 적는다. 이후 매주 같은 주소에 같은 파일로 다시 게시한다. 지난주 글은 페이지에서 뺀다. 페이지는 글마다 큰 카드를 옆으로 넘겨 보는 형태(점·n/5 표시, 좌우 버튼)이며 확대 창은 없다.
9. 메일 한 통(jaeukstark@gmail.com), 주소끼리 빈 줄 하나씩. 형식은 단순한 글만(색 버튼·그림 없음), 제목 줄 굵게. 순서: 제목 "[카쌉] 이번 주 5개 승인 요청", 승인 링크(검수 페이지 주소), 한 줄 요약(요일, 유형, 제목), "링크는 확인 화면만 열고 승인 버튼을 한 번 더 눌러야 처리돼요", 승인 마감 안내(각 글 게시 시각 전까지, 10시가 지나면 다음 주 같은 요일로 밀려요).
10. 실패하면 오류 메일 1통(원문 포함)을 보내고 멈춘다. 웹 주소 권한 오류는 30초 뒤 1번만 다시 시도한다.
11. 마무리 보고는 메일과 같은 내용으로, 마지막에 구분·내용 표.

## 하지 않는 것
인스타에 직접 게시하지 않는다(게시는 Apps Script가 승인된 글만 올린다). 토큰을 읽거나 적지 않는다. 시트의 상태를 `승인`으로 바꾸지 않는다(승인은 사용자만).
