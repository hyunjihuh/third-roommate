# 10분 무응답, 1주 만료 흐름 확인 (모의 DB/AI)
import asyncio,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844})
    await pg.add_init_script(path=os.path.join(HERE,'mock_story.js'))
    await pg.goto('file://'+os.path.join(HERE,'..','dist','index.html'))
    await pg.click('[data-act="demo"]');await pg.wait_for_timeout(1000)
    db="(await window.claude.use('db'))"
    # 1주 만료: 예시 카드 g1의 기한을 지난 것으로
    await pg.evaluate(f"(async()=>{{await {db}.doc(`rooms/${{S.code}}/agreements/g1`).update({{until:Date.now()-1000}});S.flow=null;render()}})()");await pg.wait_for_timeout(800)
    for _ in range(3):
      t=await pg.inner_text('.dialog') if await pg.query_selector('.dialog') else ''
      if '1주 해봤어요' in t: break
      for s in ['seenAgr','fyiOk','ack','ok']:
        if await pg.query_selector(f'.dialog [data-act="{s}"]'): await pg.click(f'.dialog [data-act="{s}"]');await pg.wait_for_timeout(400);break
    print('EXPIRY |',(await pg.inner_text('.dialog')).replace('\n',' / '))
    r=await pg.evaluate("(()=>{const a=S.agrs.find(x=>x.id==='g1');return [a.state, a.until<Date.now()]})()");print('agr state',r)
    # verify(): 만료된 카드는 근거로 못 씀
    v=await pg.evaluate("JSON.stringify(verify({route:'covered_by_agreement',evidence_ids:['g_g1']}))");print('VERIFY expired card ->',v)
    # 10분 무응답: 깨어 있는 룸메에게 간 편지의 전달 시각을 11분 전으로
    await pg.evaluate(f"(async()=>{{await {db}.doc(`rooms/${{S.code}}/requests/w1`).set({{from:S.seat,to:S.seat==='A'?'B':'A',kind:'do',text:'방에서 통화해도 돼?',draft:'방에서 통화해도 돼?',facts:[],translations:{{}},ts:Date.now()-11*60000,deliveredAt:Date.now()-11*60000,stage:'delivered'}});await {db}.doc(`rooms/${{S.code}}/agreements/g1`).update({{state:'off'}});S.dismissed['agrg1']=1;S.flow=null;render()}})()");await pg.wait_for_timeout(800)
    for _ in range(4):
      for s in ['seenAgr','fyiOk','ack','ok','dismissAgr']:
        if await pg.query_selector(f'.dialog [data-act="{s}"]'): await pg.click(f'.dialog [data-act="{s}"]');await pg.wait_for_timeout(400);break
    print('WAIT |',(await pg.inner_text('.dialog')).replace('\n',' / ') if await pg.query_selector('.dialog') else '(no dialog)')
    print('stage after 11min',await pg.evaluate("S.reqs.find(r=>r.id==='w1').stage"))
    await b.close()
asyncio.run(main())
