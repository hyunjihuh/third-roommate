# 공개 배포 모드(Supabase 저장소) 흐름 확인: 방 만들기 -> 초대 링크 -> 룸메 입장 -> 카드 -> 묻기 -> 답
import asyncio,os
FONTCSS=[p for p in ['/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/jua/index.css','/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/gowun-dodum/index.css'] if os.path.exists(p)]  # 오프라인 QA용 글꼴 (없으면 건너뜀)
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(HERE,'shots');os.makedirs(OUT,exist_ok=True)
URL='file://'+os.path.join(HERE,'..','dist','index.html')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844})
    await ctx.add_init_script(path=os.path.join(HERE,'mock_supabase.js'))
    pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('load',lambda *_:[asyncio.ensure_future(pg.add_style_tag(url='file://'+c)) for c in FONTCSS])
    await pg.goto(URL);await pg.wait_for_selector('[data-act="create"]');await pg.screenshot(path=OUT+'/be_01_start.png')
    await pg.click('[data-act="create"]');await pg.wait_for_selector('[data-act="shareDone"]');await pg.screenshot(path=OUT+'/be_02_share.png')
    code=await pg.evaluate("S.code");print('room',code)
    await pg.click('[data-act="shareDone"]');await pg.click('[data-act="obDone"][data-arg="cards"]');await pg.wait_for_timeout(400)
    for _ in range(6):
      await pg.click('[data-act="sort"][data-arg$="|O"]');await pg.wait_for_timeout(250)
    await pg.screenshot(path=OUT+'/be_03_cardsA.png')
    # 같은 가짜 서버를 보게 하려고 같은 페이지에서 B로 바꿔 본다 (초대 링크 화면 확인)
    await pg.evaluate("leave();window.__devA=localStorage.getItem('dev');localStorage.setItem('dev','devB')");await pg.evaluate(f"S.invite='{code}';render()");await pg.screenshot(path=OUT+'/be_04_invite.png')
    await pg.click('[data-act="join"]');await pg.wait_for_timeout(600);await pg.screenshot(path=OUT+'/be_05_B_onboard.png')
    await pg.click('[data-act="obDone"][data-arg="cards"]');await pg.wait_for_timeout(300)
    for _ in range(3):
      await pg.click('[data-act="sort"][data-arg$="|X"]');await pg.wait_for_timeout(250)
    await pg.click('[data-act="go"][data-arg="home"]');await pg.fill('#sayT','지금 방에서 통화해도 돼?');await pg.click('[data-act="say"]');await pg.wait_for_timeout(500);await pg.screenshot(path=OUT+'/be_06_B_pickKind.png')
    await pg.click('[data-act="kindDo"]');await pg.wait_for_timeout(700);await pg.screenshot(path=OUT+'/be_07_B_sent.png')
    print('reqs',await pg.evaluate("S.reqs.map(r=>r.stage+':'+r.draft)"),'cards',await pg.evaluate("S.cards.map(c=>c.id+(c.A?.v||'-')+(c.B?.v||'-')).join(' ')"))
    await pg.evaluate("leave();localStorage.setItem('dev',window.__devA)");await pg.fill('#codeT',code);await pg.click('[data-act="join"][data-arg="auto"]');print('seat after rejoin',await pg.evaluate("S.seat"));await pg.wait_for_timeout(900);await pg.screenshot(path=OUT+'/be_08_A_letter.png')
    print('A sees', await pg.inner_text('.dialog'))
    print('errors',errs)
    await b.close()
asyncio.run(main())
