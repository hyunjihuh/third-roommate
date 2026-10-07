# src 폴더의 조각을 합쳐 dist/index.html 한 장을 만든다. 실행: python3 src/build.py
import os
d=os.path.dirname(os.path.abspath(__file__))
r=lambda f:open(os.path.join(d,f),encoding='utf-8').read()
import base64,json
img={n[:-5]:'data:image/webp;base64,'+base64.b64encode(open(os.path.join(d,'img',n),'rb').read()).decode() for n in sorted(os.listdir(os.path.join(d,'img'))) if n.endswith('.webp')}
js=r('app.js').replace('__IMG__',json.dumps(img)).replace('__ICONS__',r('icons.txt')).replace('__MAPS__',r('maps.txt'))
out=r('shell.html').replace('/*CSS*/',r('style.css')).replace('/*JS*/',js)
p=os.path.join(d,'..','dist','index.html');open(p,'w',encoding='utf-8').write(out);print('built',p,len(out))
