# 허들링 앱 기획 하네스

PRD의 사용자 플로우 1개를 받아, 프로덕트 디자이너가 손으로 하던 기획 검토
5단계를 에이전트 + 게이트 + 판정 스크립트로 수행한다.
규칙 값은 이 파일에 적지 않는다. 아래 파일이 원본이다.

## 원본 문서 (읽기 전용)

- 컨텍스트·우선순위: harness/00-context.md
- 판정 기준: docs/story-service.md / 작업 재료: docs/story-work.md (둘을 섞지 않는다)
- 기능·권한·상태: docs/prd.md / 비주얼: docs/design.md
- 규칙 SSOT: harness/rules.yaml (판정 스크립트는 이 파일만 읽는다)

## 트리거

| 사용자 발화 | 동작 |
|---|---|
| "<플로우 이름> 하네스 돌려줘" | slug 변환 → 실행 루프 시작 (진행 중이면 이어서) |
| "이어서 해줘" | 가장 최근 state.json 기준 재개 |
| "판정만 돌려줘" | judge만 실행, 위반 목록 표시 |
| "승인" / "PM 확인 완료" | state.json approved=true → S5 진행 |

플로우 이름 ↔ slug: harness/03-artifacts.md. 목록에 없는 플로우는 받지 않는다.

## 실행 루프 (상세: harness/06-orchestrator.md)

1. slug 확정 → runs/<slug>/state.json 읽기 (없으면 생성)
2. 현재 단계 에이전트에게 위임
   - S1 flow-designer
   - S2 edge-case-reviewer
   - S3·S4 policy-reviewer
   - S5 ux-writer
3. 단계마다 judge 호출 (`python3 harness/judge.py <slug> <단계>`)
   - 위반 0 → 다음 단계
   - 위반 ≥ 1 → 같은 단계 재작업
   - 복귀 조건 → S1
   - 재시도·복귀 상한: rules.yaml `returns`
   - 상한 초과 → 중단하고 사람에게 묻는다
4. S4 통과 후 항상 사람 승인 1회 (`PM 확인` 행이 있으면 먼저 제시)
5. S5 통과 + approved=true → 완료 보고

단계별 입출력·복귀 조건: harness/02-pipeline.md
게이트 G1~G10: harness/04-gates.md

## 역할과 편집 범위 (상세: harness/05-roles.md)

- 작업 에이전트는 자기 산출물 파일만 수정한다 (PreToolUse 훅이 강제).
- judge는 읽기 전용이며 위반 수만 보고한다.
- state.json은 오케스트레이터(메인 세션)만 수정한다.
- docs/, harness/는 누구도 수정하지 않는다.

## 금지

- 오케스트레이터가 산출물을 직접 쓰지 않는다. 반드시 에이전트에게 위임한다.
- judge 통과 전에 다음 단계로 넘어가지 않는다.
- 피그마는 건드리지 않는다 (사람이 반영).

## 완료 보고 (5줄 이내)

- 산출물 5개 경로와 각 행 수
- 게이트 G1~G10 위반 0건
- S1 복귀 / 재작업 횟수
- `PM 확인` 처리 결과
- 사람이 할 일: 피그마 반영

## 검증·수정 (상세: harness/07-verification.md)

- 규칙 변경 → rules.yaml만 / 에이전트 방식 변경 → .claude/agents/<이름>.md만
