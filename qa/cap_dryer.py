# 슬라이드용 캡처(구현 파트까지): 이야기 두 개로 고정 (물어보기: 밤 스탠드 과제 / 부탁: 아침 드라이기). 390x844, 2배
import asyncio,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(HERE,'shots_dryer');os.makedirs(OUT,exist_ok=True)
FONTCSS=[p for p in ['/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/jua/index.css'] if os.path.exists(p)]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('load',lambda *_:[asyncio.ensure_future(pg.add_style_tag(url='file://'+c)) for c in FONTCSS])
    await pg.add_init_script(path=os.path.join(HERE,'mock_dryer.js'))
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
    # 같이 맞춰보기(드라이기): 바다는 자는 중
    await say('아침에 드라이기 소리 때문에 깨');await shot('d_clarify')
    if await has('#clT'): await pg.fill('#clT','평일 7시 반');await act('sendClarify');await pg.wait_for_timeout(800)
    await shot('d_confirm')
    await act('confirmAsk');await pg.wait_for_timeout(700);await shot('ask_queued')
    await clear();await shot('home_holding')
    await sw();await shot('B_sleeping')
    await act('setSt','in');await pg.wait_for_timeout(1500);await clear('드라이기');await shot('B_incoming')
    await act('rHard');await pg.fill('#noteT','욕실엔 콘센트가 없어서 어려워');await act('rSend');await pg.wait_for_timeout(600)
    await sw();await clear('어렵');await shot('A_reply_hard')
    await pg.click('.dialog [data-act="align"]');await pg.wait_for_timeout(900);await shot('A_constraints')
    await pg.fill('#ca0','1교시 있는 날은 7시 반까지는 자야 해');await pg.check('#cs0');await pg.fill('#ca1','소리만 작아져도 괜찮아');await pg.check('#cs1')
    await act('consSubmit');await pg.wait_for_timeout(600);await shot('A_cons_done')
    await sw();await pg.evaluate('S.c2={}');await clear('맞춰보자');await shot('B_cons_notice')
    await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(900);await shot('B_constraints')
    await pg.fill('#ca0','욕실엔 콘센트가 없어');await pg.check('#cs0');await pg.fill('#ca1','문 앞 콘센트에서 약풍으로는 할 수 있어');await pg.check('#cs1')
    await act('consSubmit');await pg.wait_for_timeout(1500)
    await sw();await pg.wait_for_timeout(1200);await clear('방법');await shot('A_options_notice')
    await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(600);await shot('A_options')
    await pg.click('[data-act="pick"][data-arg$="|0"]');await pg.wait_for_timeout(500);await shot('A_picked')
    await sw();await clear('방법')
    if await has('.dialog [data-act="go"][data-arg^="thread|"]'): await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(600)
    await shot('B_options')
    await pg.click('[data-act="pick"][data-arg$="|0"]');await pg.wait_for_timeout(1500);await shot('agreed')
    await act('go','cards');await shot('cards_with_new')
    await pg.click('[data-act="go"][data-arg^="agr|"]');await pg.wait_for_timeout(500);await shot('agr_detail')
    await say('내일 아침 7시에 문 앞에서 약풍으로 말려도 돼?');await shot('direct_by_card')
    print('prompts with C2:',[x[:60] for x in await pg.evaluate("window.__prompts.filter(p=>p.includes('[C2')).map(p=>p.slice(p.indexOf('[C2'),p.indexOf('[C2')+300))")][:2])
    print('errors',errs[:5])
    await b.close()
asyncio.run(main())
