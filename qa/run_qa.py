import asyncio,sys,json
from playwright.async_api import async_playwright
import os
FONTCSS=[p for p in ['/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/jua/index.css','/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/gowun-dodum/index.css'] if os.path.exists(p)]  # 오프라인 QA용 글꼴 (없으면 건너뜀)
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'shots');os.makedirs(OUT,exist_ok=True)
CHECK=r"""()=>{const bad=[];const vw=innerWidth,vh=innerHeight;document.querySelectorAll('#app *').forEach(el=>{const cs=getComputedStyle(el);if(cs.display==='none'||el.closest('.vh')||el.closest('svg'))return;const r=el.getBoundingClientRect();if(!r.width||!r.height)return;
 if(el.scrollWidth>el.clientWidth+1&&cs.overflowX!=='auto'&&cs.overflowX!=='scroll'&&el.clientWidth>0&&!el.matches('.world,.stage,.scene,.m'))bad.push('가로넘침 '+el.tagName+'.'+el.className+' '+(el.innerText||'').slice(0,30));
 if(r.right>vw+1&&!el.closest('.world'))bad.push('화면밖 '+el.tagName+'.'+el.className+' '+(el.innerText||'').slice(0,30)+' r='+Math.round(r.right));});return [...new Set(bad)].slice(0,15)}"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for vw,vh in [(390,844),(360,640)]:
      pg=await b.new_page(viewport={'width':vw,'height':vh})
      errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('load',lambda *_:[asyncio.ensure_future(pg.add_style_tag(url='file://'+c)) for c in FONTCSS]);pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
      await pg.add_init_script(path=os.path.join(HERE,'mock.js'))
      await pg.goto('file://'+os.path.join(HERE,'..','dist','index.html'))
      i=[0]
      async def sw():
        await pg.click('[data-act="go"][data-arg="home"]');await pg.wait_for_timeout(200);await pg.click('[data-act="go"][data-arg="me"]');await pg.wait_for_timeout(200);await pg.click('[data-act="switchSeat"]');await pg.wait_for_timeout(600)
      async def shot(name):
        await pg.wait_for_timeout(350);i[0]+=1
        f=f'{OUT}/{vw}_{i[0]:02d}_{name}.png';await pg.screenshot(path=f)
        bad=await pg.evaluate(CHECK)
        print(f'[{vw}] {i[0]:02d} {name}',('문제: '+' | '.join(bad)) if bad else 'ok')
      async def act(a,arg=None):
        sel=f'[data-act="{a}"]'+(f'[data-arg="{arg}"]' if arg else '')
        await pg.click(sel);await pg.wait_for_timeout(300)
      async def say(txt):
        await act('go','home')
        if await has('[data-act="seenAgr"]'): await act('seenAgr')
        await pg.fill('#sayT',txt);await act('say');await pg.wait_for_timeout(600)
      async def has(sel): return await pg.query_selector(sel) is not None
      await shot('start')
      await act('demo');await shot('home_A')
      await act('go','cards');await shot('cards')
      await pg.click('.grid .tile');await shot('card_detail');await act('back')
      await say('지금 방에서 10분 통화');await shot('direct')
      if await has('[data-act="why"]'): await act('why')
      await shot('direct_why');await act('ok')
      await say('친구 데려와도 돼?');await shot('clarify')
      await pg.fill('#clT','10시까지');await act('sendClarify');await pg.wait_for_timeout(600);await shot('clarify_after');
      if await has('[data-act="ok"]'): await act('ok')
      await say('내일 아침 8시 방에서 과외 1시간');await shot('delivered_queued')
      await act('ok')
      await act('go','letters');await shot('letters_A')
      await pg.click('[data-act="go"][data-arg^="thread|"]');await shot('thread_A')
      await act('go','home');await act('go','me');await shot('me_A');await act('switchSeat');await pg.wait_for_timeout(400);await shot('home_B_sleeping')
      await act('cycle');await pg.wait_for_timeout(800);await shot('home_B_letter')
      # 쌓인 편지 처리: 과외 편지가 나올 때까지
      for _ in range(4):
        if await has('#noteT'):
          txt=await pg.inner_text('.dialog')
          if '과외' in txt: break
          await act('rOk');await pg.wait_for_timeout(500)
          if await has('[data-act="ok"]'): await act('ok')
        elif await has('[data-act="fyiOk"]'): await act('fyiOk');await pg.wait_for_timeout(400)
        else: break
      await shot('home_B_letter2')
      await pg.fill('#noteT','9시 이후면 괜찮아');await act('rHard');await pg.wait_for_timeout(400);await shot('B_after_reply')
      await sw();await shot('A_reply')
      await pg.click('[data-act="align"]');await pg.wait_for_timeout(600);await shot('A_constraints')
      await pg.fill('#ca0','학생이 8시만 돼');await pg.check('#cs0');await pg.fill('#ca1','장소는 바꿀 수 있어');await pg.check('#cs1')
      await pg.click('[data-act="consSubmit"]');await pg.wait_for_timeout(500);await shot('A_cons_done')
      await sw();await shot('B_home_cons')
      for _ in range(3):
        if await has('#noteT'):
          await act('rOk');await pg.wait_for_timeout(500)
          if await has('[data-act="ok"]'): await act('ok')
          if await has('[data-act="toCards"].choice, .dialog [data-act="ok"]'): pass
      await shot('B_home_cons2')
      await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(600)
      await pg.fill('#ca0','8시엔 자고 있어');await pg.check('#cs0');await pg.fill('#ca1','비밀 이유');
      await pg.click('[data-act="consSubmit"]');await pg.wait_for_timeout(500);await shot('B_cons_done')
      await sw();await pg.wait_for_timeout(800)
      for _ in range(4):
        if await has('.dialog [data-act="ack"]'): await act('ack');await pg.wait_for_timeout(700)
        elif await has('.dialog [data-act="ok"]'): await act('ok')
        elif await has('.dialog [data-act="toCards"]') and await has('.dialog [data-act="ok"]'): await act('ok')
        else: break
      await shot('A_options_home')
      await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(400);await shot('A_options_thread')
      await pg.click('[data-act="pick"][data-arg$="|0"]');await pg.wait_for_timeout(300)
      await sw()
      await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(300);await shot('B_options_thread')
      await pg.click('[data-act="pick"][data-arg$="|0"]');await pg.wait_for_timeout(900);await shot('agreed')
      await act('go','home');await shot('home_after_agree')
      if await has('[data-act="ok"]'): await act('ok')
      await act('go','cards');await shot('cards_with_trial')
      await pg.click('[data-act="go"][data-arg^="agr|"]');await shot('trial_card_detail')
      await sw()
      await say('내일 아침 8시 스터디룸에서 과외');await shot('direct_by_trial_card')
      if await has('[data-act="why"]'): await act('why');await shot('direct_by_trial_why')
      if await has('[data-act="ok"]'): await act('ok')
      await say('아침 드라이기 때문에 짜증나');await shot('ask_clarify')
      if await has('#clT'):
        await pg.fill('#clT','7시 반');await act('sendClarify');await pg.wait_for_timeout(600)
      await shot('ask_confirm')
      if await has('[data-act="confirmAsk"]'): await act('confirmAsk');await pg.wait_for_timeout(500);await shot('ask_sent')
      await act('go','letters');await shot('letters_end')
      await act('go','home');await act('go','me');await shot('me')
      print('JS 오류:',errs[:5])
      await act('leave');await act('create','A');await pg.wait_for_timeout(500);await shot('share')
      await act('shareDone');await shot('onboard')
      await act('obDone','cards');await shot('sort_new')
      await act('sort');await shot('sort_new2')
      await act('go','cards');await shot('cards_new')
      await act('go','home');await shot('home_new')
    await b.close()
asyncio.run(main())
