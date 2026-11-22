"""검수 아티팩트 HTML 만들기.
사용: python3 ruee_build_review.py TEMPLATE.html IMAGE_ROOT OUT.html S004 S005 S006 ...
IMAGE_ROOT/<시리즈>/01~08.jpg 를 작게 줄여 페이지에 넣는다(__IMGS__ 자리).
"""
import base64, io, json, os, sys
from PIL import Image
tpl, root, out, series = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
imgs = {}
for s in series:
    arr = []
    for i in range(1, 11):
        p = os.path.join(root, s, f'{i:02d}.jpg')
        if not os.path.exists(p): break
        im = Image.open(p).convert('RGB').resize((432, 540), Image.LANCZOS); b = io.BytesIO(); im.save(b, 'JPEG', quality=72, optimize=True)
        arr.append('data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode())
    if len(arr) in (8, 10): imgs[s] = arr
open(out, 'w').write(open(tpl).read().replace('__IMGS__', json.dumps(imgs)))
print('ok', list(imgs))
