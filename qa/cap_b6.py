# 슬라이드용 캡처: 이야기 두 개로 고정 (물어보기: 밤 스탠드 과제 / 부탁: 아침 드라이기). 390x844, 2배
import asyncio,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(HERE,'shots_find');os.makedirs(OUT,exist_ok=True)
FONTCSS=[p for p in ['/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/jua/index.css'] if os.path.exists(p)]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('load',lambda *_:[asyncio.ensure_future(pg.add_style_tag(url='file://'+c)) for c in FONTCSS])
    await pg.add_init_script(path=os.path.join(HERE,'mock_story.js'))
    await pg.goto('file://'+os.path.join(HERE,'..','dist','index.html'))
    async def has(s): return await pg.query_selector(s) is not None
    async def act(a,arg=None):
      await pg.click(f'[data-act="{a}"]'+(f'[data-arg="{arg}"]' if arg else ''));await pg.wait_for_timeout(350)
    async def shot(name):
      await pg.wait_for_timeout(500);await pg.screenshot(path=f'{OUT}/{name}.png');d=await pg.inner_text('.dialog') if await has('.dialog') else ''
      print(name,'|',d.replace('\n',' / ')[:110])
    async def sw():
      await act('go','home');await act('go','me');await act('switchSeat');await pg.wait_for_timeout(900)
    async def dlg(): return await pg.inner_text('.dialog') if await has('.dialog') else ''
    async def clear(until=None):
      for _ in range(6):
        t=await dlg()
        if until and until in t: return
        if await has('.dialog [data-act="seenAgr"]'): await act('seenAgr')
        elif await has('.dialog [data-act="fyiOk"]'): await act('fyiOk')
        elif await has('.dialog [data-act="ack"]'): await act('ack')
        elif await has('.dialog [data-act="ok"]'): await act('ok')
        else: return
    async def say(t):
      await act('go','home');await clear()
      if not await has('#sayT'): await act('talk')
      await pg.fill('#sayT',t);await act('say');await pg.wait_for_timeout(800)
    await act('demo');await pg.wait_for_timeout(800)
    await pg.evaluate("window.__del(/\\/agreements\\/g1$|\\/requests\\/d3$/)");await pg.wait_for_timeout(500)

    async def fresh():
      await pg.goto('file://'+os.path.join(HERE,'..','dist','index.html'));await pg.wait_for_timeout(500)
      await act('demo');await pg.wait_for_timeout(800)
      await pg.evaluate("window.__del(/\\/agreements\\/g1$|\\/requests\\/d3$/)");await pg.wait_for_timeout(500)
      await pg.evaluate("(async()=>{const db=await window.claude.use('db');await db.doc(`rooms/${S.code}`).update({status:{A:'in',B:'in'}})})()");await pg.wait_for_timeout(400);await clear()
    await pg.evaluate("(async()=>{const db=await window.claude.use('db');await db.doc(`rooms/${S.code}`).update({status:{A:'in',B:'in'}})})()");await pg.wait_for_timeout(400);await clear()
    await sw();await clear()
    await say('아침마다 알람 좀 줄여줄 수 있어? 가능하면 ㅠㅠ');await pg.wait_for_timeout(500);await shot('f1_b6_confirm')
    await pg.fill('.dialog textarea','나 아침마다 알람 소리에 계속 깨서 좀 힘들어 ㅠㅠ 가능하면 알람 두 번까지만 맞춰줄 수 있을까?');await pg.wait_for_timeout(300);await shot('f1_b6_edited')
    print('errors',errs[:5])
    await b.close()
asyncio.run(main())
