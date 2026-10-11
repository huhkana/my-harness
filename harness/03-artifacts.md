# 03. 산출물

## 저장 위치와 파일명

```
runs/<플로우-slug>/
  s1-flow.md               화면 플로우
  s2-edge-cases.md         엣지케이스 목록
  s3-impact.md             영향 범위 메모
  s4-policy-conflicts.md   정책 충돌 목록
  s5-ux-writing.md         UX 라이팅 문구표
  state.json               진행 상태
```

## 플로우 slug (고정)

| 플로우 | slug |
|---|---|
| 무료 콘텐츠 탐색 | free-browse |
| 유료 자료 열람 | paid-library |
| 스킬 카드 사용 | skill-card |
| 미션 제출 | mission-submit |
| 내 자산 등록 | asset-register |
| 판매 신청 | sale-request |
| 운영자 검수 | admin-review |

## 산출물 형식

- 파일마다 고정 컬럼 표 1개.
- 근거 컬럼이 있는 파일은 모든 행에 PRD 섹션 번호를 적는다 (예: `6-5`).

| 파일 | 필수 컬럼 |
|---|---|
| s1-flow.md | 화면ID · 화면명 · 진입 조건(role) · 컴포넌트 · 다음 화면 · 근거 |
| s2-edge-cases.md | ID · 상황 · 관련 상태값 · 처리 · 화면 추가 필요(Y/N) · 근거 |
| s3-impact.md | ID · 영향받는 플로우/기능 · 영향 내용 · 근거 |
| s4-policy-conflicts.md | ID · 충돌 정책 · 처리 방향(유지/플로우 변경/PM 확인) · 근거 |
| s5-ux-writing.md | 화면ID · 위치 · 문구 · 상태값 · accent(Y/N) |

## 규칙 SSOT

- `harness/rules.yaml` 1개. 판정 스크립트는 이 파일만 읽는다.
- 담는 것: 산출물별 필수 컬럼, design.md 토큰 허용값, 어기면 안 되는 것 검사 항목, 복귀 조건.
- 구체 값은 R5에서 채운다.

## 재개

- 가능. `state.json`에 기록:
  - `stage`: 현재 단계 (S1~S5)
  - `s1_returns`: S1 복귀 횟수 (최대 2)
  - `approved`: 사람 승인 여부
- 재실행 시 첫 번째 미완료/실패 단계부터 시작.
