# 피그마 보고서 슬라이드 작업 지시 (Step 2 통합 보고서, v3)

## 절대 규칙
- 피그마 fileKey `yFW9Ge0Wbr1Mlk9UbD4lS5`, 페이지 `85:2`. **자기에게 배정된 섹션 안에만 쓴다.** 다른 섹션(은지 것: 01-07)은 읽지도 고치지도 않는다. 섹션 자체의 위치, 크기, 이름도 건드리지 않는다.
- KO 섹션 id `257:2`, EN 섹션 id `257:3`. 슬라이드 총 22장, 번호(1-22)는 아래 목록 그대로. START = (맡은 첫 슬라이드 번호 - 1).
- 먼저 ToolSearch로 `select:mcp__Figma__use_figma,mcp__Figma__get_figma_skill,mcp__Figma__get_screenshot` 로드, 그다음 `get_figma_skill`로 `skill://figma/figma-use/SKILL.md`를 읽는다. use_figma 호출마다 `skillNames:"resource:figma-use,resource:figma-generate-design"`.
- 렌더러는 `/home/claude/handoff/docs/figma_slides/helper.js`를 **그대로** 쓴다(디자인 통일). 호출 코드 = `const SEC_ID="...", START=n, TOTAL=22; const SPECS=[...];` + helper.js 전문. 한 호출에 4-6장씩. 코드 5만 자 제한.
- 반환값의 `left`(남은 세로 px)가 음수면 넘친 것. 내용을 줄여서(문장 줄이기, 행 빼기, `fs` 낮추기) 그 프레임만 지우고(`(await figma.getNodeByIdAsync(id)).remove()`, 자기가 만든 id만) 같은 START로 다시 만든다. 장마다 get_screenshot(maxDimension 900, enableBase64Response true)으로 한 번 확인.
- 끝나면 만든 프레임 id 목록과 확인 못 한 점만 짧게 보고.

## 스펙 형식 (helper.js)
슬라이드: `{s:'섹션 라벨', t:'제목(= 이 장의 메시지 한 문장)', l:'리드 한두 줄(선택)', b:[블록...], n:'아래 강조 한 줄(선택)', name:'프레임 이름(선택)', ts:제목 크기(기본 36, 길면 30)}`
블록:
- `{k:'cards', c:[[태그, 제목, 본문, 꼬리(선택)],...], g:1}` 2-5칸 카드. `g:1`이면 남는 세로 공간만큼 늘어남
- `{k:'flow', c:[[태그, 제목, 본문],...]}` 화살표로 이어지는 단계 (최대 6)
- `{k:'table', w:[열 비율], h:[머리], r:[[칸...],...], fs:15, tight:1}` 첫 열 굵게
- `{k:'big', c:[[큰 숫자, 설명],...]}`
- `{k:'code', h:'라벨', t:'여러 줄 텍스트', fs:13.5}` 어두운 상자 (JSON, 프롬프트 발췌)
- `{k:'shots', h:380, c:[[파일 이름, 캡션 제목, 캡션],...]}` 화면 캡처 자리 (그림은 나중에 사람이 넣음)
- `{k:'text', t:'...', fs:15}`
- `{k:'cols', w:[비율], c:[블록 또는 [블록들], ...]}` 좌우 나누기
폭 1424px, 본문에 쓸 수 있는 높이는 대략 600px(리드, 노트 있으면 더 적음). 표는 6-7행까지.

## 디자인, 글 규칙
- "올레 사업계획서" 느낌: 여백 많고 한 장에 메시지 하나. 제목이 곧 결론 문장. 카드 안 글은 2-4줄. 꽉 채우지 않는다.
- 섹션 라벨: KO `01  문제 정의` / `02  관련 연구` / `03  에이전트 설계` / `04  구현` / `05  마무리`. EN `01  PROBLEM` / `02  RELATED WORK` / `03  AGENTIC DESIGN` / `04  IMPLEMENTATION` / `05  WRAP-UP`.
- 긴 대시(—) 금지, 하이픈(-)이나 쉼표. 과장 금지. 확인 안 된 걸 된 것처럼 쓰지 않는다. 효과가 입증됐다는 표현 금지(Step 3에서 볼 것).
- KO는 "~다" 평서체, 은지 보고서 문장을 최대한 살린다(아래 "은지 원문"). EN은 평이한 학술 영어.
- 앱 안 용어: 우리 방(Our Room) / 편지(Letters) / 카드(Cards) / 같이 만든 카드(co-made card, 1-week trial) / 요정 보라(Bora, the room fairy) / "보라에게 말하기"(Tell Bora) / 같이 맞추기(Align together).
- 참고문헌 번호: [1] Bae CHI'25, [2] Ha CHI EA'25, [3] Garcia Ayala FAccT'26, [4] Liu ACL Findings'26, [5] Cheng arXiv'26, [6] W3 강의, [7] Clark et al. 2020, [8] Niu & Brown 2016.

## 자료 (읽을 것)
- `/home/claude/handoff/docs/기획서_v3.html` 0장(지금 버전 요약, 기능 목록), 1.2, 2.5, 5.5(근거 표), 8.1
- `/home/claude/handoff/qa/C1_실제모델_시험_1008.md`
- `/home/claude/handoff/src/app.js` 160-300행 근처(프롬프트 C0-C7 원문, 출력 JSON), `verify(` 함수
- `/home/claude/handoff/README_인수인계.md` (구조, stage, 모델 vs 코드 표)
- `/home/claude/handoff/supabase/functions/claude/index.ts`
- 과제 안내: `/root/.claude/uploads/5f0b4b9c-4e81-5c9c-8a2b-c6e8350675c2/f9d6af69-attachment.txt`

## 사실 (틀리면 안 됨)
- 공개 URL: https://third-roommate.netlify.app (설치, 로그인 없음. 첫 화면 "혼자 둘러보기"로 데모 방, 설정에서 "B 화면으로 보기")
- 스택: HTML 한 장 + 바닐라 JS(Netlify) / Supabase Postgres(`docs` 표: path, room, data jsonb) + Realtime / Supabase Edge Function `claude`가 OpenAI 호출. 키는 서버에만. 판단과 대안(C1, C4)은 gpt-4.1, 문장 작업(C0, C2, C3, C6, C7, 말투 변환)은 gpt-4.1-mini, temperature 0.2, JSON 출력 강제. 서버 하루 1500건, 방 한 사람 하루 20건 제한.
- 탭 3개: 우리 방 / 편지 / 카드. 입구는 입력창 하나.
- 시작 카드 6장 = Niu & Brown(2016) 기숙사생 503명 조사의 갈등 원인 상위 6개: 개인 공간(내 책상이나 침대 쓰기), 잠(내가 잘 때 불 켜기), 소리(밤에 방에서 통화), 청결(방에서 냄새 나는 음식), 손님(친구 데려오기), 물건(내 물건 빌려 쓰기). + 잠긴 기숙사 규칙 카드 2장(외부인 숙박, 자정 이후 큰 소리).
- 카드마다 각자 "먼저 물어봐줘 / 그냥 해도 돼"(+ 조건: 15분 이내, 23시 전, 미리 말하면 등). 둘 다 정하기 전엔 서로 안 보임.
- C1 출력: kind(permission|request), route(covered_by_agreement|clarification_needed|coordination_needed), evidence_ids, missing_fields, clarification, hour, minutes, weekend, reason, unsafe. 코드 verify(): 근거 카드 둘 다 O인지, 시간 조건, 제안 카드 아님, 기숙사 규칙 카드면 rule, 같이 만든 카드면 체험 기간 안인지. 하나라도 어긋나면 "룸메에게 묻기"로 내린다. AI 실패 시에도 전부 묻기. AI 실패로 허락이 나는 길은 없다.
- 길 6개: 바로 답(direct) / 알림만(fyi: "미리 말하면" 조건이나 체험 카드) / 한 번 되묻기 / 룸메에게 묻기(자는 중이면 queued, 깨면 delivered) / 기숙사 규칙(rule, 멈춤) / unsafe(전달 안 하고 사감실, 상담센터 안내).
- stage: direct / fyi / rule / queued → delivered → replied → done | constraints → aligning → agreed / blocked / cancelled
- 같이 맞추기: 답이 "이번엔 어려워요"면 C2가 역할(부탁한 사람 / 받은 사람)에 따라 다른 질문 1-2개를 각자에게만 → "알려도 돼요" 체크한 답만 본인 말 그대로 저장(C3는 구조화만, 뜻을 바꾸지 않음) → C4가 대안 최대 3개(대안마다 누가 무엇을 맞추는지) → 같은 버전의 같은 안을 둘 다 골라야 합의 → C6 합의문 → "같이 만든 카드"(1주 체험) → 다음에 같은 요청이 오면 그 카드로 바로 답하고 상대에겐 알림만 → 1주 뒤 계속 / 바꾸기 / 그만하기. 3번 안 맞으면 직접 얘기하라고 멈춤. C7은 끝난 일에서 새 카드 제안(둘 다 정하기 전엔 근거로 안 씀).
- C0: 불편이나 부탁을 보낼 문장으로 다듬고 본인이 고쳐 승인한 것만 전달. 처음 적은 말은 저장 안 함. 말투 변환: 받는 사람이 고른 말투(부드럽게 / 직설적으로)로, 사실 칩과 "보낸 그대로 보기" 같이.
- 상태(깨어 있음 / 자는 중)는 본인이 직접 설정. 센서, 추론 없음. 룸메가 자는 중이면 요정이 룸메 침대에서 잔다. 방 그림은 시간대 3장(아침, 저녁, 밤).
- C1 실제 모델 시험(2026.10.08, 14문장, 한 번씩): 고치기 전 8/14 → 고친 뒤 13/14, 잘못 허락 0건. 고친 것: 판단 순서 5단계 + 예시 3개(few-shot), 코드에서 근거 제목→id 보정. 남은 1건은 허락해도 되는 걸 묻는 쪽(안전한 방향). 일관성(반복 실행)은 아직 안 봄.
- 확인한 것(실제 서버): 방 만들기와 초대 링크, 바로 답(약 2초), 룸메에게 묻기, C0 다듬기, 말투 변환, C2 질문. 자동 QA(가짜 AI)로 전체 흐름 41화면. 아직 못 한 것: 실제 서버에서 대안 → 둘 다 선택 → 같이 만든 카드까지 끝에서 끝, 두 기기 동시 실시간, 사용자 연구(Step 3).
- 계정 없음: 방 코드가 열쇠(링크를 아는 사람만). 한계로 적는다.
- AI 활용: 런타임 = OpenAI gpt-4.1 / gpt-4.1-mini(교수님 제공 키). 그림(방 3장, 요정 6포즈, 카드 18장, 우표) = ChatGPT 이미지 생성, 실행 중엔 이미지 AI 안 씀. 코딩과 QA 스크립트, 기획서 정리 = Claude. 보고서 문헌 확인, 한영 작성, 도식, 피그마 배치 = Codex(은지 기재)와 Claude(이 v3 슬라이드). 프롬프트 C0-C7 초안 = 은지 + AI, 실제 모델 시험 후 팀이 수정. 주제, 컨셉, 상호작용, 최종 판단과 책임 = 팀. 기여 비율 숫자는 적지 않는다.
- W3 강의 실제 제목: "W3. Large Language Models & Prompt Engineering (Part 2)" 안의 Collaboration 장(Elicit individual views → Synthesize → Evaluate/Critique → Incorporate dissent → Revise → Find common ground, "Better result ≠ better collaboration", Prompt Arena 전략: user & role modeling, representation & interaction, agency & adaptation, multi-turn orchestration). 프롬프트 기법: 프롬프트 체인, 구조화 출력(JSON), few-shot, 판단 순서 명시.

## 슬라이드 22장
1. 표지 (완료, KO)
2. 목차 (완료, KO)
3. [01] 문제 정의: "사소해서 묻기 어렵고, 안 물으면 눈치가 보인다". 카드 4: 대상 사용자 / 맥락 / 문제 / 바라는 결과. 노트 = 은지의 디자인 질문.
4. [01] Why not ChatGPT: "범용 챗봇은 한 사람의 말만 듣고, 묻는 일은 여전히 사용자 몫이다". 표: 필요한 능력 | 범용 챗봇 | 우리 방 요정. 행: 두 사람의 맥락 유지 / 다단계 조율 / 대화 밖 행동(자는 중 보류, 깬 뒤 전달, 체험 만료 재검토) / 둘 다의 동의. 노트: 에이전트가 늘 낫다고 가정하지 않는다. 카드 안의 일은 모델 판단 없이 룸메가 미리 한 결정으로 끝낸다.
5. [02] 관련 연구 종합 표: 흐름 | 무엇을 했나 | 남은 어려움 | 우리 설계. 행: 가사 협업 [1] / 신뢰와 입장 대표 [2,3,5] / 선제적 중재 [4,5] / 룸메 갈등 원인과 규칙 [7,8].
6. [02] "연구에서 가져온 세 가지 방향": 카드 3 (은지 06: 개별 관점 수집 / 의견 종합과 수정 / 참여자의 결정권) + 노트(검토한 연구만으로 룸메 장기 조율 효과는 확립 안 됨).
7. [03] 컨셉: "미리 같이 정해둔 허락을 요정이 들고 다닌다". 카드 3: 우리 방(상태) / 카드(같이 정한 허락) / 편지(전달과 조율). 노트: 허락을 내리는 건 요정의 판단이 아니라 룸메가 미리 한 결정.
8. [03] 에이전트 흐름: flow 6단계 User → Understand(C1) → Plan(길 정하기 + 코드 확인) → Act(바로 답 / 전달 / 보류) → Observe(룸메 답, 상태 변화, 체험 기간) → Adapt(같이 만든 카드, 카드 제안). 아래에 한 줄 예시("내일 아침 8시 방에서 과외" 사례가 여섯 단계를 어떻게 도는지).
9. [03] 요청 분기: "모델은 제안하고, 코드가 허용한다". 표: 길 | 언제 | 사용자에게 보이는 것 | 코드가 확인하는 것 (6행).
10. [03] 같이 맞추기: "각자 따로 묻고, 같은 안을 둘 다 골라야 합의다". flow 5-6단계 + 아래 카드 2-3(침묵은 동의가 아니다 / 버전 / 3번 안 되면 멈춤).
11. [03] W3 개념 → 설계 결정 → 왜 중요한가 표(6-7행). 은지 07-02 표와 기획서 2.5를 합친다.
12. [03] 주요 설계 근거 표: 근거(종류 표시: 논문 / 사전 조사 / 팀 판단) | 결정 | 왜 중요한가. 기획서 5.5에서 6-7행 고른다(입구 하나, 시작 카드 6장, 모델은 제안 코드가 확인, 침묵은 대기, 자는 중 보류, 본인이 승인한 문장만, 같이 만든 카드).
13. [04] 시스템 구조: flow 또는 cols로 브라우저(Netlify) ↔ Supabase(Postgres + Realtime) ↔ Edge Function ↔ OpenAI. 아래 카드: 저장소 / 실시간 / 키와 제한 / AI가 안 될 때.
14. [04] 프롬프트 체인 표: 호출 | 입력 | 출력(JSON 필드) | 코드가 확인. C1, C0, C2, C3, C4, C6, C7, 말투 변환 (8행, fs 13.5, tight).
15. [04] 상태와 데이터: 카드 3 (개인 맥락 / 요청 맥락 / 합의 맥락, 은지 07-02) + stage 전이 한 줄(code 블록) + 데이터 경로(rooms/{코드}, /cards, /requests, /agreements).
16. [04] 중간 표현: cols 좌 code(C1 실제 출력 JSON 예시, app.js 191행 예시 사용) 우 code 또는 카드(verify 뒤의 결과: route, checks 목록). 제목 "모델 출력은 JSON이고, 화면에 가기 전에 코드가 한 번 더 본다".
17. [04] C1 시험: big 3개(8/14 → 13/14 / 잘못 허락 0건 / 14문장) + 표 4-5행(대표 문장: 고치기 전 → 고친 뒤) + 노트(한 번씩만 돌림).
18. [04] 프롬프트 설계 디테일: C1 프롬프트 발췌(code: [판단 순서] 5단계 요약 + [예시] 1개) 와 카드 3(판단 순서 명시 / few-shot / 저장 기록은 참고만).
19. [04] 화면: shots 4 (h 400): `390_02_home_A.png` 우리 방 / `390_11_thread_A.png` 편지 / `390_03_cards.png` 카드 / `390_24_A_options_thread.png` 같이 맞추기. 캡션 한 줄씩.
20. [04] 구현 현황과 공개 URL: 카드 3 (확인한 것 / 아직 못 한 것 / 써보는 법: URL, 혼자 둘러보기, 둘이 쓰기).
21. [05] 한계와 Step 3 계획: 카드 3 (은지 17: 기능 검증 / 사용자 연구(최소 3명) / 설계의 한계) + 우리 한계(계정 없음, 미국 기숙사 조사 기반 카드, 모델 일관성).
22. [05] AI 활용 명세 + 참고문헌: cols 좌 표(무엇에 | 도구 | 팀이 한 일) 우 text(참고문헌 [1]-[8], fs 12). 좁으면 표를 줄인다.

EN은 1번 표지, 2번 목차도 만든다(KO 표지 스펙: `{k:'cover',name:'Cover',s:'ID40018 Mini Project 1  ·  Step 2 Combined Report',t:'The Third Roommate',t2:'우리 방 요정',l:'A shared agent that carries small permissions and requests between roommates. ...',team:'Hyunji Huh  ·  Eunji Shin  ·  Inseong Seo',url:'Prototype  third-roommate.netlify.app',date:'2026.10.08'}`, 목차는 cards 5칸 g:1).

## 은지 원문 (KO, 최대한 살릴 것)
- 대상 사용자: 기숙사나 집을 함께 쓰는 대학생. 친한 친구일 수도 있고, 함께 살며 처음 알아가는 사이일 수도 있다.
- 사용 맥락: 수면, 통화, 과외, 드라이기 사용, 청소, 손님 초대, 음식과 공용 공간 사용 등 일상에서 반복된다.
- 조율의 어려움: 사소한 불편은 꺼내기 어렵다. 침묵은 동의로 오해되고, 처음의 "다 괜찮아"를 나중에 바꾸기도 어색하다.
- 디자인 질문: 작은 요청을 매번 대립으로 만들지 않으면서, 생활 경계를 표현하고 합의를 다시 조정하게 하려면?
- 설계 목표 3: 불편 사항의 표현 / 상호 이해 / 합의의 실행 가능성. "위 내용은 설계 목표와 향후 평가 기준이며, 효과가 입증됐다는 뜻은 아니다."
- 에이전트 요구사항: 맥락 유지(일회성 챗봇 답변은 이 맥락을 사용자가 다시 전달하고 맞춰야 한다) / 다단계 조율(조언 생성 이후에도 두 사람 사이의 절차를 이어가야 한다) / 개입 시점(자는 동안 요청 대기, 상태 변경 후 전달, 합의 만료 시 재검토 제안). "가장 가벼운 경로부터: 현재 유효한 공동 승인 조건에 맞으면, 협상을 다시 열지 않고 그 근거를 설명한다."
- 관련 연구: 가사 협업 [1] 효율성뿐 아니라 가사 노동의 의미와 서로의 노력에 대한 인정이 중요하다 → 각자의 조정을 보여주되, 잘못 점수나 양보 빚 장부로 만들지 않는다. / 신뢰와 입장 표현 [2,3,5] 공정성, 중재자의 감독, 개별 입장이 전달되는 방식이 중재 경험에 영향을 준다 → 비공개 입력과 승인된 공유 문장을 분리하고, 사용자가 수정하게 한다. / 선제적 중재 [4,5] 개입 시점을 고르고 드러나지 않은 관점을 끌어내는 접근이 시도됐다 → 개입 시점을 확인, 제어하게 하고, 합의를 강제하지 않으며 이견을 남긴다. / "검토한 연구만으로 룸메이트의 장기적 일상 조율 효과는 확립되지 않는다. 커플, 전문 중재, 모의 협상, 학생 팀의 결과를 이 맥락에서 검증해야 한다."
- 설계 근거: 개별 관점 수집(필요한 조건을 각자에게 묻고, 공유를 승인한 내용만 전달한다. 조용하거나 말하기 어려운 사람도 즉시 대면하지 않고 의견을 낼 수 있다) / 의견 종합과 수정(대안별 조정 부담을 보여주고, 조건 추가나 거절을 허용한다. 이견을 지우지 않으면서 수정 과정을 통해 합의를 만든다) / 참여자의 결정권(같은 대안에 두 사람이 동의해야 한다. 에이전트는 돕고, 사람이 결정한다. 대화가 부드러워져도 한 사람의 결정권이 줄어들면 충분하지 않다). "참여, 입장 반영, 공정성, 합의의 질, 만족도를 따로 살핀다. 빠른 합의가 곧 좋은 협업은 아니다. [6]"
- 개념 → 결정 → 영향(은지 07-02): 맥락 유지와 다단계 조율 → 입구 하나 + 요청 단위 상태 관리 → 반복 설명과 화면 이동 감소 / 개별 관점과 반대 의견 보존 → 비공개 질문 → 공유 승인 → 조건 비교 → 말하기 어려운 필요도 반영 / 공통 기반과 반복 숙의 → 대안 제안 → 같은 안에 양측 승인 → AI의 제안과 사람의 결정을 구분 / 개입 시점과 사용자 통제 → 수면 중 보류, 동의한 시점에 후속 확인 → 불필요한 방해와 알림 부담 조절 / 시간에 따른 적응 → 시험 적용 피드백으로 합의 수정 제안 → 과거 수락을 영구 규칙으로 확대하지 않음.
- 맥락 3종: 개인 맥락(원문, 개인 조건, 공유 선택. 승인 전에는 상대에게 전달하지 않음) / 요청 맥락(요청 ID, 응답, 대안, 현재 단계. 대안 버전별로 양측 승인 상태 관리) / 합의 맥락(범위, 기간, 조건, 검토일, 상태).
- 평가 계획과 한계: 기능 검증(의도 분기, 승인 후 전달, 조건 변경, 버전 불일치, 무응답, 시험 합의 만료) / 사용자 연구(최소 3명이 프로토타입을 사용하고 짧은 인터뷰. 누가 말하고 수정하고 거절하는지, 입장이 누락됐다고 느끼는지 관찰) / 설계의 한계(중립적인 촉진자와 개인의 대변자, 유용한 기억과 감시감, 적시 개입과 방해 사이의 긴장. 절차 완료나 빠른 합의만으로 관계가 개선됐다고 판단하지 않는다).
- 참고문헌 전문:
[1] Bae, G., Park, S. K., Kim, T., & Hong, H. (2025). Exploring Design Spaces to Facilitate Household Collaboration for Cohabiting Couples. CHI '25. https://doi.org/10.1145/3706598.3713383
[2] Ha, J., Kim, S., Lim, H. S., Kim, D., Lee, B., & Oh, C. (2025). My Agent or Yours? Exploring Emotional and Moral Responses in Multi-Agent Conflict Situations. CHI EA '25, Article 410. https://doi.org/10.1145/3706599.3721237
[3] Garcia Ayala, J. F., Wee, P., Abouzied, A., & Goyal, N. (2026). MedAIting with the Mediators: Exploring Aligned Agent Interventions to Resolve Challenges in Mediator Workflows. FAccT '26, 1424-1453. https://doi.org/10.1145/3805689.3806726
[4] Liu, Z., Sarrafzadeh, B., Zhou, P., Yang, L., Zhao, J., & Sharma, A. (2026). ProMediate: A Simulation Testbed for Evaluating Proactive Mediation in Multi-Party Negotiation. Findings of ACL 2026, 29570-29598. https://aclanthology.org/2026.findings-acl.1479/
[5] Cheng, C.-J., Chung, Y.-C., Chiu, B.-C., Lin, Y.-H., & Liao, J.-W. (2026). Exploring AI-Supported Disciplinary Mediation in Student Project Teams' Text-Based Communication. arXiv preprint. https://arxiv.org/abs/2608.07503
[6] ID40018 Data-Driven AI Service Design. (2026). W3. Large Language Models & Prompt Engineering (Part 2). Course material.
[7] Clark et al. (2020). 쉐어하우스 거주자 37명 인터뷰. (서지 확인 필요)
[8] Niu & Brown (2016). UW-Madison 기숙사 7곳 503명 설문, 룸메 갈등 원인 상위 8개. Peer Relations Study Group 연구 요약. (서지 확인 필요)
[7], [8]의 저자 이름이나 제목을 지어내지 않는다. 위에 적힌 대로만 쓴다.
