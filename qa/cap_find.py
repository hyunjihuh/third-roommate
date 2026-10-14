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
    # F1 털어놓는 칸: 바다 비공개 질문에 쓰고 체크 안 함
    await pg.evaluate("(async()=>{const db=await window.claude.use('db');await db.doc(`rooms/${S.code}`).update({status:{A:'in',B:'in'}})})()");await pg.wait_for_timeout(400);await clear()
    await say('오늘 밤 12시 넘어서 스탠드 켜고 과제해도 돼?');await clear()
    await sw();await clear('스탠드')
    if await has('[data-act="rHard"]'): await act('rHard');await pg.fill('#noteT','12시엔 자야 해서 불빛 보이면 깨');await act('rSend');await pg.wait_for_timeout(600)
    await sw();await clear('어렵');await pg.click('.dialog [data-act="align"]');await pg.wait_for_timeout(900)
    await pg.fill('#ca0','내일 마감이라 오늘은 꼭 끝내야 해');await pg.check('#cs0');await act('consSubmit');await pg.wait_for_timeout(600)
    await sw();await pg.evaluate('S.c2={}');await clear('맞춰보자');await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(900)
    await pg.fill('#ca0','밤 12시부터는 스탠드가 꺼져 있었으면 좋겠어. 솔직히 3주째 참고 있었어');await pg.evaluate("document.querySelector('#ca0').scrollIntoView({block:'center'})");await shot('f1_vent')
    # F3 미안해: 바다가 받는 편지
    await fresh()
    await say('술 좀 마셨는데 새벽 3시쯤 들어갈듯 최대한 조용히 들어갈게 ㅈㅅ');await clear()
    await sw();await pg.wait_for_timeout(1500);await clear('3시');await shot('f3_sorry')
    # F3 초대: 부탁으로 도착
    await fresh()
    await say('토요일에 치이카와 영화 보러 갈래??? 내가 예매할게!!');await shot('f3_invite_confirm')
    if await has('[data-act="confirmAsk"]'): await act('confirmAsk');await pg.wait_for_timeout(700)
    await sw();await pg.wait_for_timeout(1500);await clear('치이카와');await shot('f3_invite_in')
    # F4 카드 제안
    await fresh()
    await pg.evaluate("(async()=>{const db=await window.claude.use('db');await db.doc(`rooms/${S.code}/cards/pz`).set({cat:'물건',title:'이름 붙은 음식은 먹기 전에 묻기',icon:'fridge',flavor:'지난번 일에서 생긴 제안 카드.',origin:'proposal',proposal:{rationale:'',conditions:'',exceptions:'',source_case_id:'d1'},A:null,B:null,createdAt:Date.now()})})()");await pg.wait_for_timeout(500)
    await act('go','cards');await shot('f4_cards_banner')
    await pg.evaluate("go('sort')");await pg.wait_for_timeout(500)
    for _ in range(8):
      if 'proposal' in (await pg.evaluate("(()=>{const me=S.seat;const t=S.cards.filter(c=>!c[me]&&!c.locked)[0];return t?t.origin:''})()")): break
      await pg.evaluate("(async()=>{const db=await window.claude.use('db');const me=S.seat;const t=S.cards.filter(c=>!c[me]&&!c.locked)[0];await db.doc(`rooms/${S.code}/cards/${t.id}`).update({[me]:{v:'X',cond:''}})})()");await pg.wait_for_timeout(400)
    await shot('f4_proposal')
    # 관계 거리: 같은 방에서 보낸 배달, 아직 답이 없어요
    await fresh()
    await pg.evaluate("(async()=>{const db=await window.claude.use('db');await db.doc(`rooms/${S.code}/requests/w9`).set({from:'A',to:'B',kind:'ask',text:'지금 배달 시킬 건데 같이 먹을래?',draft:'지금 배달 시킬 건데 같이 먹을래?',facts:['배달','지금'],translations:{},ts:Date.now()-11*60000,deliveredAt:Date.now()-11*60000,stage:'delivered'})})()");await pg.wait_for_timeout(800);await act('go','home');await clear('아직');await shot('rel_no_reply')
    print('errors',errs[:5])
    await b.close()
asyncio.run(main())
