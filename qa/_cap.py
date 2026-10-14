import asyncio,sys,json
from playwright.async_api import async_playwright
import os
FONTCSS=[p for p in ['/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/jua/index.css','/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/gowun-dodum/index.css'] if os.path.exists(p)]  # 오프라인 QA용 글꼴 (없으면 건너뜀)
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'shots2x_c');os.makedirs(OUT,exist_ok=True)
CHECK=r"""()=>{const bad=[];const vw=innerWidth,vh=innerHeight;document.querySelectorAll('#app *').forEach(el=>{const cs=getComputedStyle(el);if(cs.display==='none'||el.closest('.vh')||el.closest('svg'))return;const r=el.getBoundingClientRect();if(!r.width||!r.height)return;
 if(el.scrollWidth>el.clientWidth+1&&cs.overflowX!=='auto'&&cs.overflowX!=='scroll'&&el.clientWidth>0&&!el.matches('.world,.stage,.scene,.m'))bad.push('가로넘침 '+el.tagName+'.'+el.className+' '+(el.innerText||'').slice(0,30));
 if(r.right>vw+1&&!el.closest('.world'))bad.push('화면밖 '+el.tagName+'.'+el.className+' '+(el.innerText||'').slice(0,30)+' r='+Math.round(r.right));});return [...new Set(bad)].slice(0,15)}"""
FAILS=[]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for vw,vh in [(390,844)]:
      pg=await b.new_page(viewport={'width':vw,'height':vh},device_scale_factor=2)
      errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('load',lambda *_:[asyncio.ensure_future(pg.add_style_tag(url='file://'+c)) for c in FONTCSS]);pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
      await pg.add_init_script(path=os.path.join(HERE,'mock.js'))
      await pg.goto('file://'+os.path.join(HERE,'..','dist','index.html'))
      i=[0]
      async def sw():
        await pg.click('[data-act="go"][data-arg="home"]');await pg.wait_for_timeout(200);await pg.click('[data-act="go"][data-arg="me"]');await pg.wait_for_timeout(200);await pg.click('[data-act="switchSeat"]');await pg.wait_for_timeout(600)
      async def shot(name):
        await pg.wait_for_timeout(350);i[0]+=1
        f=f'{OUT}/{vw}_{i[0]:02d}_{name}.png';await pg.screenshot(path=f,full_page=name in ('A_constraints','B_constraints','cards_new','cards_with_trial'))
        bad=await pg.evaluate(CHECK)
        print(f'[{vw}] {i[0]:02d} {name}',('문제: '+' | '.join(bad)) if bad else 'ok')
      async def act(a,arg=None):
        sel=f'[data-act="{a}"]'+(f'[data-arg="{arg}"]' if arg else '')
        await pg.click(sel);await pg.wait_for_timeout(300)
      async def say(txt):
        await act('go','home')
        if await has('[data-act="seenAgr"]'): await act('seenAgr')
        if not await has('#sayT'): await act('talk')
        await pg.fill('#sayT',txt);await act('say');await pg.wait_for_timeout(600)
      async def has(sel): return await pg.query_selector(sel) is not None
      async def check(label,must=(),mustnot=(),sel='#app',cond=None):
        t=await pg.inner_text(sel) if await has(sel) else ''
        bad=[f'없음 "{m}"' for m in must if m not in t]+[f'있으면 안 됨 "{m}"' for m in mustnot if m in t]
        if cond is not None and not cond: bad.append('조건 실패')
        print(f'[{vw}]   확인 {label}:',('통과' if not bad else '실패 '+', '.join(bad)))
        if bad: FAILS.append(f'[{vw}] {label}: '+', '.join(bad))
      import re
      async def no_raw_ab(label):
        t=await pg.inner_text('#app')
        m=re.search(r'(^|[^A-Za-z0-9])[AB](가|는|이|를|의|에게) ',t)
        await check(label+' (A, B 글자 없음)',cond=m is None)
      await shot('start')
      await act('demo');await shot('home_A')
      await act('go','cards');await shot('cards')
      await pg.click('.grid .tile');await shot('card_detail');await act('back')
      await pg.click('.grid .tile:has-text("밤늦게")');await shot('card_detail_mine');await act('back')
      await say('지금 방에서 10분 통화');await shot('direct')
      if await has('[data-act="why"]'): await act('why')
      await shot('direct_why');await act('ok')
      await say('친구 데려와도 돼?');await shot('clarify')
      await pg.fill('#clT','10시까지');await act('sendClarify');await pg.wait_for_timeout(600);await shot('clarify_after');
      if await has('[data-act="ok"]'): await act('ok')
      await say('내일 아침 8시 방에서 과외 1시간');await shot('delivered_queued')
      await act('ok');await shot('home_holding')
      await act('go','letters');await shot('letters_A')
      await check('편지 목록: 바로 답은 보라가 답한 것으로',must=['보라가 바로 답함'])
      await pg.click('[data-act="go"][data-arg^="thread|"]');await shot('thread_A')
      await check('편지 화면: 지금 단계 표시',cond=await has('.stline'))
      await check('편지 화면: "상대" 대신 이름',mustnot=['상대에게'])
      await act('go','home');await act('go','me');await shot('me_A');await act('switchSeat');await pg.wait_for_timeout(400);await shot('home_B_sleeping')
      await check('내가 자는 중: 불 끈 방 + 내 침대 z + 보라는 안 잠 + 입력창 없음 + 깨기 버튼',must=['나는 자는 중이에요','일어났어'],cond=(not await has('#sayT')) and ('t-night' in (await pg.get_attribute('.room','class'))) and await has('.sleeper') and not await has('.elf-sleep'))
      await check('둘러보기: 끝내기 버튼 + 알림 종',cond=await has('.demo-end') and await has('.bell'))
      await pg.click('.hud [data-act="setSt"]');await pg.wait_for_timeout(300);await pg.wait_for_timeout(800);await shot('home_B_letter')
      await check('깨면: 요정도 깨서 편지를 들고 옴',mustnot=['나는 자는 중이에요'],cond=not await has('.sleeper'))
      # 쌓인 편지 처리: 과외 편지가 나올 때까지
      for _ in range(4):
        if await has('[data-act="rOk"]'):
          txt=await pg.inner_text('.dialog')
          if '과외' in txt: break
          await act('rOk');await pg.wait_for_timeout(500)
          if await has('[data-act="ok"]'): await act('ok')
        elif await has('[data-act="fyiOk"]'): await act('fyiOk');await pg.wait_for_timeout(400)
        else: break
      await shot('home_B_letter2')
      await act('rHard');await check('어렵다고 고르면 이유 칸이 열림',must=['이유를 한마디'])
      await pg.fill('#noteT','9시 이후면 괜찮아');await act('rSend');await pg.wait_for_timeout(400);await shot('B_after_reply')
      await sw();await shot('A_reply')
      await check('A 대화창: 전해 들은 말투',must=['어렵대요'],sel='.dialog')
      await pg.click('[data-act="align"]');await pg.wait_for_timeout(600);await shot('A_constraints')
      await check('편지의 답장: 바다 본인의 말',must=['어려울 것 같아.'],mustnot=['어렵대요','이번엔 어려워'])
      await check('조건 질문 화면: 공유 체크',must=['꼭 반영되었으면 하는 답에만 체크'],mustnot=['대안 만들 때 써도 돼요'])
      await pg.fill('#ca0','학생이 8시만 돼');await pg.check('#cs0');await pg.fill('#ca1','장소는 바꿀 수 있어');await pg.check('#cs1')
      await pg.click('[data-act="consSubmit"]');await pg.wait_for_timeout(500);await shot('A_cons_done')
      await sw();await shot('B_home_cons')
      for _ in range(3):
        if await has('[data-act="rOk"]'):
          await act('rOk');await pg.wait_for_timeout(500)
          if await has('[data-act="ok"]'): await act('ok')
          if await has('[data-act="toCards"].choice, .dialog [data-act="ok"]'): pass
      await shot('B_home_cons2')
      await check('B: 맞춰보기 질문 이유',must=['같이 맞춰보자고 했어요'],sel='.dialog')
      await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(600);await shot('B_constraints')
      await pg.fill('#ca0','8시엔 자고 있어');await pg.check('#cs0');await pg.fill('#ca1','비밀 이유');
      await pg.click('[data-act="consSubmit"]');await pg.wait_for_timeout(500);await shot('B_cons_done')
      await sw();await pg.wait_for_timeout(800)
      for _ in range(4):
        if await has('.dialog [data-act="ack"]'):
          await shot('A_reply_seen');await act('ack');await pg.wait_for_timeout(700);await shot('A_after_ack')
        elif await has('.dialog [data-act="ok"]'): await act('ok')
        elif await has('.dialog [data-act="toCards"]') and await has('.dialog [data-act="ok"]'): await act('ok')
        else: break
      await shot('A_options_home')
      await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(400);await shot('A_options_thread')
      await pg.click('[data-act="pick"][data-arg$="|0"]');await pg.wait_for_timeout(300);await shot('A_picked')
      await sw()
      await pg.click('.dialog [data-act="go"][data-arg^="thread|"]');await pg.wait_for_timeout(300);await shot('B_options_thread')
      await check('B 대안: 하늘이 뭘 골랐는지는 아직 안 보임',must=['골랐어요 (내가 고르면 보여요)'],mustnot=['하늘 고름','버전'])
      await check('B 대안: 같은 제목 두 번 없음',cond=(await pg.locator('text=과외는 거실 스터디룸에서').count())==1)
      await check('B 대안: 얻음 줄 없음',mustnot=['얻음'])
      await pg.click('[data-act="pick"][data-arg$="|0"]');await pg.wait_for_timeout(900);await shot('agreed')
      await check('합의 알림: 카드 보기',must=['카드 보기'],sel='.dialog')
      await no_raw_ab('합의 알림')
      await act('go','home');await shot('home_after_agree')
      if await has('[data-act="ok"]'): await act('ok')
      await act('go','cards');await shot('cards_with_trial')
      await pg.click('[data-act="go"][data-arg^="agr|"]');await shot('trial_card_detail')
      await check('막 만든 카드엔 "1주 더" 없음',mustnot=['1주 더'],must=['어땠는지 물어볼게요'])
      await no_raw_ab('같이 만든 카드')
      await sw()
      await say('내일 아침 8시 스터디룸에서 과외');await shot('direct_by_trial_card')
      if await has('[data-act="why"]'): await act('why');await shot('direct_by_trial_why')
      if await has('[data-act="ok"]'): await act('ok')
      await say('아침 드라이기 때문에 짜증나');await shot('ask_clarify')
      if await has('#clT'):
        await pg.fill('#clT','7시 반');await act('sendClarify');await pg.wait_for_timeout(600)
      await shot('ask_confirm')
      if await has('[data-act="confirmAsk"]'): await act('confirmAsk');await pg.wait_for_timeout(500);await shot('ask_sent')
      if await has('.dialog [data-act="ok"]'): await act('ok')
      await sw();await pg.wait_for_timeout(1200)
      for _ in range(3):
        t=await pg.inner_text('.dialog') if await has('.dialog') else ''
        if '드라이기' in t: break
        if await has('[data-act="fyiOk"]'): await act('fyiOk')
        elif await has('.dialog [data-act="ok"]'): await act('ok')
        else: break
      await shot('wish_B_incoming')
      if await has('[data-act="rCond"]'):
        await act('rCond');await pg.wait_for_timeout(300)
        if await has('#noteT'): await pg.fill('#noteT','7시 반 전엔 욕실에서 말려줘')
        await shot('wish_B_cond')
        if await has('[data-act="rSend"]'): await act('rSend');await pg.wait_for_timeout(500)
      await sw();await pg.wait_for_timeout(800);await shot('wish_A_reply')
      if await has('.dialog [data-act="ack"]'): await act('ack');await pg.wait_for_timeout(800);await shot('wish_A_done')
      await act('go','letters');await shot('letters_end')
      await act('go','home');await act('go','me');await shot('me')
      await check('내 프로필: 자라기와 소품',must=['소품','다음:'])
      print('JS 오류:',errs[:5])
      await act('leaveAsk');await check('방 나가기 확인',must=['다시 들어오려면 방 코드'])
      await act('leave');await check('첫 화면 (둘러보기 방은 최근 방에 안 남김)',must=['혼자 둘러보기'],mustnot=['최근 방'])
      await act('create','A');await pg.wait_for_timeout(500);await shot('share')
      await act('shareDone');await shot('onboard')
      await act('obDone','cards');await shot('sort_new')
      await check('룸메가 없을 땐 "룸메가"',must=['룸메가 이걸 하고 싶을 때'],mustnot=['B가'])
      await pg.click('[data-act="sort"][data-arg$="|O"]');await pg.wait_for_timeout(300);await shot('sort_O_cond')
      await check('그냥 해도 돼를 고르면 조건 칸이 나옴',must=['대신 지켜줬으면 하는 게 있어?','저장하고 다음 카드'])
      await act('sortSave');await shot('sort_new2')
      await act('go','cards');await shot('cards_new')
      await act('go','home');await shot('home_new')
      await check('새 방 홈: 초대 안내',must=['룸메 아직 안 들어옴','룸메가 아직 방에 안 들어왔어요'])
    await b.close()
asyncio.run(main())
print('\n확인 실패:',len(FAILS))
for f in FAILS: print(' -',f)
sys.exit(1 if FAILS else 0)
