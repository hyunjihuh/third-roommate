# 18번 슬라이드용: 예시 방 홈에서 보라에게 말 걸기 입력창 연 화면
import asyncio,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(HERE,'shots_story')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    FONTCSS=[p for p in ['/tmp/claude-0/-home-claude/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/scratchpad/fonts/node_modules/@fontsource/jua/index.css'] if os.path.exists(p)]
    pg.on('load',lambda *_:[asyncio.ensure_future(pg.add_style_tag(url='file://'+c)) for c in FONTCSS])
    await pg.add_init_script(path=os.path.join(HERE,'mock_story.js'))
    await pg.goto('file://'+os.path.join(HERE,'..','dist','index.html'))
    await pg.click('[data-act="demo"]');await pg.wait_for_timeout(1000)
    await pg.evaluate("window.__del(/\\/agreements\\/g1$|\\/requests\\/d3$/)");await pg.wait_for_timeout(500)
    for _ in range(4):
      for s in ['seenAgr','fyiOk','ack','ok']:
        if await pg.query_selector(f'.dialog [data-act="{s}"]'): await pg.click(f'.dialog [data-act="{s}"]');await pg.wait_for_timeout(400)
    if not await pg.query_selector('#sayT'): await pg.click('[data-act="talk"]');await pg.wait_for_timeout(500)
    await pg.wait_for_timeout(500);await pg.screenshot(path=f'{OUT}/home_talk.png');print(await pg.inner_text('.dialog'))
    await b.close()
asyncio.run(main())
