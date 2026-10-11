# 화면 플로우 — sale-request

| 화면ID | 화면명 | 진입 조건(role) | 컴포넌트 | 다음 화면 | 근거 |
|---|---|---|---|---|---|
| SR-01 | 내 자산 상세 | paid, seller | button-primary, button-outline | SR-02 | 6-5 |
| SR-02 | 판매 신청 작성 | seller | text-input, button-primary | SR-03 | 6-5, 7-4 |
| SR-03 | 판매 신청 상태 | seller | badge-overlay | — | 6-5 |
| SR-04 | 검수 승인 처리 | seller | button-primary | — | 6-7 |
| SR-05 | 수정 요청 확인 | seller | faq-row | SR-02 | 6-5 |
