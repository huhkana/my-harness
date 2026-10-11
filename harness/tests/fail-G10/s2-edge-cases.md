# 엣지케이스 목록 — sale-request

| ID | 상황 | 관련 상태값 | 처리 | 화면 추가 필요(Y/N) | 근거 |
|---|---|---|---|---|---|
| E1 | 판매 승인 전 유료 회원이 공개 범위에서 판매 신청 선택 | role=paid, visibility=sale_requested | 선택지 비활성 + 안내 문구 | N | 7-4 |
| E2 | 첨부 파일 용량 초과 | review_status=draft | 업로드 차단 | N | 6-7 |
| E3 | 수정 요청 받은 자산 재제출 | review_status=revision_requested | 수정 후 다시 검수 대기 | N | 6-5 |
