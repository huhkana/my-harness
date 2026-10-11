# 05. 역할

## 작업 에이전트 (4개)

story-work.md의 넘김 지점(2·4·5번)을 경계로 나눈다. 정의 파일: `.claude/agents/<이름>.md`

| 에이전트 | 단계 | 대신하는 사람 | 편집 범위 (이것만 수정 가능) |
|---|---|---|---|
| flow-designer | S1 (S1 복귀 포함) | 프로덕트 디자이너 | runs/*/s1-flow.md |
| edge-case-reviewer | S2 | 개발자 (2번 넘김) | runs/*/s2-edge-cases.md |
| policy-reviewer | S3 + S4 | PM·정책 담당자 (4번 넘김) | runs/*/s3-impact.md, runs/*/s4-policy-conflicts.md |
| ux-writer | S5 | 개발자·피그마 핸드오프 (5번 넘김) | runs/*/s5-ux-writing.md |

## 읽기 전용 판정자

| 에이전트 | 도구 | 하는 일 |
|---|---|---|
| judge | Read, `python3 harness/judge.py <slug> <단계>` | rules.yaml 기준 위반 수 보고. 산출물 수정 불가 |

- judge.py는 Python 표준 라이브러리만 사용 (rules.yaml은 내장 간이 파서로 읽음, PyYAML 불필요).

## 편집 범위 강제

- R4 구조(runs/<slug>/ 안 파일 5개)를 유지하고, 폴더 대신 파일 단위로 범위를 나눈다.
- PreToolUse 훅이 위 표의 범위 밖 파일 수정(Write/Edit)을 차단한다.
- docs/, harness/는 모든 에이전트에게 읽기 전용.
- state.json은 오케스트레이터(메인 세션)만 수정한다.

## 자연어 트리거

| 사용자 발화 | 동작 |
|---|---|
| "<플로우 이름> 하네스 돌려줘" (예: "판매 신청 하네스 돌려줘") | slug 변환 → S1부터 시작, 진행 중이면 이어서 |
| "이어서 해줘" | state.json 기준 가장 최근 플로우 재개 |
| "판정만 돌려줘" | judge만 실행, 위반 목록 표시 |
| "승인" / "PM 확인 완료" | state.json approved=true → S5 진행 |
