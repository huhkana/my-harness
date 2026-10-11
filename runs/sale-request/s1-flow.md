# 화면 플로우 — sale-request

| 화면ID | 화면명 | 진입 조건(role) | 컴포넌트 | 다음 화면 | 근거 |
|---|---|---|---|---|---|
| SR-01 | 내 자산 목록 | paid, seller | nav-pill, segmented-control, ex-app-shell-row, badge-overlay, ex-empty-state-card, button-primary | SR-02 (자산 선택) / SR-06 (seller, 검수 상태 배지 선택) | 6-5, 7-3, 7-4 |
| SR-02 | 내 자산 상세 | paid, seller | ex-app-shell-row, badge-overlay, brand-chip, button-primary, button-outline | SR-03 (공개 범위 변경) / SR-01 (뒤로) | 6-5, 16 |
| SR-03 | 공개 범위 선택 | paid, seller | segmented-control, segmented-control-active, button-primary, button-outline, ex-toast | paid: 비공개·멤버 공개만 선택 가능 → SR-02 (저장) / seller: 판매 신청 선택 → SR-04 | 6-5, 7-3, 7-4, 14 |
| SR-04 | 판매 신청 정보 입력 | seller | text-input, text-input-focused, brand-chip, ex-app-shell-row, button-primary, button-outline, ex-toast | SR-05 (제출) / SR-01 (임시저장, draft) | 3-4, 6-5, 7-4, 8 |
| SR-05 | 판매 신청 제출 확인 | seller | ex-modal-card, button-primary, button-outline | SR-06 (제출 → pending) / SR-04 (돌아가 수정) | 6-7, 14, 9 |
| SR-06 | 판매 신청 상태 확인 | seller | ex-app-shell-row, badge-overlay, segmented-control, ex-empty-state-card | SR-04 (draft 이어 쓰기) / SR-07 (revision_requested) / SR-08 (approved·rejected) | 6-5, 6-8, 7-4, 8 |
| SR-07 | 수정 요청 확인 | seller | ex-app-shell-row, badge-overlay, button-primary | SR-04 (수정 후 재제출) | 6-5, 6-7, 6-8 |
| SR-08 | 검수 결과 확인 | seller | ex-app-shell-row, badge-overlay, button-outline | SR-01 (approved는 MVP 최종 상태) / SR-02 (rejected 자산 상세) | 6-5, 6-8, 9 |
