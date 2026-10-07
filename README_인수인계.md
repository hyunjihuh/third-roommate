# 우리 방 요정 (The Third Roommate) 인수인계

ID40018 Mini Project 1, Step 2 프로토타입. 2026.10.08 기준 v3.
작성: 허현지 (Claude와 같이 코딩). 보고서 기준은 신은지 Step 2 보고서 (피그마 P1 파일, P2 페이지).

## 1. 지금 어디 있나

| 무엇 | 위치 |
|---|---|
| 앱 한 장 (이걸 호스팅에 올림) | `dist/index.html` |
| 코드 조각 (고칠 때) | `src/` → `python3 src/build.py` 로 다시 합침 |
| 그림 | `src/img/` (방 3장, 요정 6포즈, 카드 18장, 우표). ChatGPT 이미지 생성으로 만들고 build.py가 앱 안에 넣음 |
| 저장소 | Supabase 프로젝트 `third-roommate` (현지 계정, hyunjihuh's Org). 표 구조는 `supabase/schema.sql` |
| AI 서버 함수 | Supabase Edge Function `claude`. 키는 대시보드 → Edge Functions → Secrets 의 `OPENAI_KEY` (지금 연결됨). `ANTHROPIC_API_KEY`만 있으면 Claude로 동작 |
| 기획서 | `docs/기획서_v3.html` (0장이 지금 버전 요약) |
| 자동 QA | `qa/` |

## 2. 여는 법

- 호스팅된 주소로 열면: 로그인 없이 동작. 방 만들기 → 초대 링크 복사 → 룸메가 링크로 들어옴
- `dist/index.html`을 파일로 열어도 같은 Supabase에 붙는다 (인터넷 필요)
- Supabase가 안 닿으면 자동으로 "로컬 모드"(이 브라우저 안에서만 저장, AI 없음)
- claude.ai 아티팩트로 올리면 아티팩트 DB와 Claude를 쓴다 (로그인 필요, 예전 방식)
- 혼자 테스트: 첫 화면 "혼자 둘러보기" → ⚙ → "B 화면으로 보기". 예시 편지 3통과 체험 카드 1장이 들어 있다

## 3. 구조

```
화면 (render)
 ├─ 우리 방: 방 그림 + 대화창. 입력창 하나("보라에게 말하기")
 ├─ 편지: 내 차례 / 지난 편지 → 편지 타임라인 (threadView)
 ├─ 카드: 2칸 격자 (같이 만든 카드 → 넘긴 카드 → 기숙사 규칙), 안 넘긴 카드는 "넘기기" 화면
 └─ ⚙ 설정: 듣는 말투 2종, 내 상태, 방 코드, 기록 내보내기

데이터 (경로는 전부 rooms/{코드}/...)
 rooms/{코드}            상태, 말투, 하루 횟수
 .../cards               허용 카드 (A, B 선택과 조건, 제안 카드, 잠긴 규칙 카드)
 .../requests            요청 하나의 전체 흐름 (stage)
 .../agreements          같이 만든 카드 (1주 체험)

저장소 연결 (src/app.js 위쪽): supaDB / localDB / claude.use("db") 셋이 같은 모양
 doc(path).get/set/update/onSnapshot, collection(path).doc/add/orderBy/limit/onSnapshot
```

stage: direct (바로 답) / fyi (알림만) / rule (기숙사 규칙) / queued → delivered → replied → done | constraints → aligning → agreed / blocked / cancelled

## 4. 모델이 하는 것 vs 코드가 확인하는 것

| 호출 | 모델 출력 | 코드가 확인 |
|---|---|---|
| C1 읽기와 분기 | kind (permission / request), route, evidence_ids, hour, minutes | 근거 카드 둘 다 O, 시간 조건(`condOK`), 제안 카드 아님, 규칙 카드, 체험 카드는 켜져 있고 기간 안 → 하나라도 어긋나면 룸메에게 묻기 |
| C0 부탁 다듬기 | draft, clarification, key_facts | 원문 저장 안 함, 사용자가 승인한 문장만 전달 |
| C2, C3 각자 조건 | questions / constraints | "알려도 돼요" 체크한 답만 저장 |
| C4 대안 | 최대 3개 | 없으면 멈춤, 버전 번호 |
| C6 합의문 | agreement_text | 같은 버전의 같은 안을 둘 다 골랐을 때만 카드로 저장 |
| C7 카드 제안 | proposal / no_proposal | 둘 다 넘기기 전엔 근거로 안 씀 |
| 말투 변환 | 받는 사람 말투 문장 | 사실 칩과 "보낸 그대로 보기" 항상 같이 |

AI가 안 되면 판단이 필요한 건 전부 룸메에게 묻기로 간다.

## 5. QA

```
pip install playwright && python3 -m playwright install chromium
python3 qa/run_qa.py        # 가짜 DB, 가짜 AI로 전체 흐름 41개 화면, 390px과 360px
python3 qa/run_backend.py   # Supabase 흉내로 방 만들기 → 초대 → 입장 → 묻기
```
글꼴은 주아(Jua) 하나고 CDN에서 받는다.

## 6. 남은 일

1. 호스팅 주소로 A, B 두 기기 실제 테스트 (실시간, 초대 링크, AI 응답 속도)
2. C1 정확도: 실제 모델로 20개 문장 확인 (지금 OpenAI 모델로 은지 프롬프트를 돌림)
3. 은지 보고서 반영 (은지 결정): 기획서 0장 끝과 5.6 목록
4. 기획서 3, 4장에 남은 옛 버전 설명 정리 (각 절 위에 "v3에서 바뀜" 표시해둠)

## 7. 주의

- 은지 피그마(P2)는 은지 담당. 고칠 게 있으면 기획서에 적고 은지에게 전달
- 방 코드가 곧 열쇠다 (로그인 없음). 링크는 연구 참여자에게만
- 기록 내보내기는 원문과 공유 안 한 조건을 저장하지 않는다. Step 3 로그로 쓸 것


## 8. 내 Supabase로 옮겨서 다시 배포하기

지금 배포본(https://third-roommate.netlify.app)은 현지 Supabase에 붙어 있다. 다른 계정으로 옮기려면:

1. Supabase에서 새 프로젝트를 만들고 SQL Editor에서 `supabase/schema.sql`을 통째로 실행한다 (표 `docs`, 권한, `doc_merge`, 실시간, 하루 횟수 `ai_tick`).
2. `supabase/functions/claude/index.ts`를 Edge Function 이름 `claude`로 올린다 (대시보드 → Edge Functions → Deploy, 또는 `supabase functions deploy claude`). JWT 확인은 끈다.
3. 대시보드 → Edge Functions → Secrets에 `OPENAI_KEY`를 넣는다. 키는 여기에만 둔다. 코드나 채팅에 붙이지 않는다.
4. `src/shell.html`의 `window.ROOM_BACKEND={url:"...",key:"..."}`를 새 프로젝트의 URL과 공개 키(anon / publishable)로 바꾼다. 이 키는 브라우저에 보여도 되는 키다.
5. `python3 src/build.py` → `dist/index.html` 한 장이 나온다.
6. 그 파일 하나를 Netlify(Deploys 화면에 끌어다 놓기)나 아무 정적 호스팅에 올린다.

확인: 첫 화면에 "AI가 아직 연결 전이에요"가 안 뜨면 서버 함수까지 붙은 것이다. 뜨면 2, 3번을 다시 본다.
같은 브라우저의 탭 두 개는 같은 기기로 인식돼 같은 사람으로 들어간다. 두 사람 테스트는 시크릿 창이나 다른 브라우저로 한다.
