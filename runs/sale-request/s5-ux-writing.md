# UX 라이팅 문구표 — sale-request

| 화면ID | 위치 | 문구 | 상태값 | accent(Y/N) |
|---|---|---|---|---|
| SR-01 | 상단 제목 | 내 자산 | role=paid, role=seller | N |
| SR-01 | 탭(segmented-control) | 전체 · 비공개 · 멤버 공개 · 판매 신청 | visibility=private, visibility=member_only, visibility=sale_requested | N |
| SR-01 | 배지(badge-overlay) | 비공개 | visibility=private | N |
| SR-01 | 배지(badge-overlay) | 멤버 공개 | visibility=member_only | N |
| SR-01 | 배지(badge-overlay) | 임시저장 | review_status=draft | N |
| SR-01 | 배지(badge-overlay) | 검수 대기 | review_status=pending | N |
| SR-01 | 배지(badge-overlay) | 수정 요청 | review_status=revision_requested | N |
| SR-01 | 배지(badge-overlay) | 승인됨 | review_status=approved | Y |
| SR-01 | 배지(badge-overlay) | 반려됨 | review_status=rejected | N |
| SR-01 | 안내 배너(role 회수, P01) | 판매 승인이 해제되어 진행 중이던 판매 신청이 모두 종료됐어요. 해당 자산은 비공개로 돌아갔어요. | role=paid, visibility=private | N |
| SR-01 | 빈 상태 제목(ex-empty-state-card) | 아직 등록한 자산이 없어요 | role=seller, visibility=private | N |
| SR-01 | 빈 상태 본문(ex-empty-state-card) | 자산을 등록하면 공개 범위를 정하고 판매 신청도 할 수 있어요. | role=seller | N |
| SR-01 | CTA | 자산 등록하기 | role=seller | N |
| SR-01 | 진입 안내(비회원) | 로그인하면 내 자산을 볼 수 있어요. | role=guest | N |
| SR-01 | 진입 안내(무료 회원) | 내 자산은 유료 멤버십 회원이 쓸 수 있어요. | role=free | N |
| SR-02 | 섹션 라벨 | 공개 범위 | role=paid, role=seller | N |
| SR-02 | CTA | 공개 범위 변경 | role=paid, role=seller | N |
| SR-02 | 보조 버튼(button-outline) | 편집 | role=seller | N |
| SR-02 | 잠금 안내(검수 대기) | 검수 중에는 수정하거나 공개 범위를 바꿀 수 없어요. | review_status=pending | N |
| SR-02 | 수정 전 안내(승인 자산, P04) | 수정하면 이 자산은 판매 자산에서 내려가고 다시 검수를 받아요. 승인본은 따로 남지 않아요. | review_status=approved | N |
| SR-02 | 수정 전 안내 확인 버튼(button-outline) | 수정하고 다시 검수 받기 | review_status=approved | N |
| SR-02 | 진입 차단 안내(ex-toast) | 판매 신청은 운영진 승인을 받은 회원만 할 수 있어요. 승인 요청은 기존 채널로 해주세요. | role=paid, visibility=sale_requested | N |
| SR-03 | 상단 제목 | 공개 범위 | role=paid, role=seller | N |
| SR-03 | 옵션(segmented-control) | 비공개 | visibility=private | N |
| SR-03 | 옵션 설명 | 나만 볼 수 있어요. | visibility=private | N |
| SR-03 | 옵션(segmented-control) | 멤버 공개 | visibility=member_only | N |
| SR-03 | 옵션 설명 | 유료 멤버십 회원이 볼 수 있어요. | visibility=member_only | N |
| SR-03 | 옵션(segmented-control) | 판매 신청 | visibility=sale_requested | N |
| SR-03 | 옵션 설명 | 운영진 검수를 통과하면 판매 자산이 돼요. | role=seller, visibility=sale_requested | N |
| SR-03 | 비활성 옵션 안내(ex-toast) | 판매 신청은 운영진 승인을 받은 회원만 할 수 있어요. 승인 요청은 기존 채널로 해주세요. | role=paid, visibility=sale_requested | N |
| SR-03 | 전환 전 안내(멤버 공개→판매 신청, P02) | 판매 신청으로 바꾸면 다른 멤버는 이 자산을 더 이상 볼 수 없어요. | visibility=member_only, visibility=sale_requested | N |
| SR-03 | 잠금 안내(검수 대기) | 검수 중에는 공개 범위를 바꿀 수 없어요. | review_status=pending | N |
| SR-03 | CTA(비공개·멤버 공개) | 저장 | visibility=private, visibility=member_only | N |
| SR-03 | CTA(판매 신청) | 다음 | role=seller, visibility=sale_requested | N |
| SR-03 | 보조 버튼(button-outline) | 취소 | role=paid, role=seller | N |
| SR-03 | 저장 완료(ex-toast) | 공개 범위를 저장했어요. | visibility=private, visibility=member_only | N |
| SR-04 | 상단 제목 | 판매 신청 정보 | role=seller, review_status=draft | N |
| SR-04 | 입력 라벨(text-input) | 사용 방법 | review_status=draft | N |
| SR-04 | 입력 라벨(text-input) | 결과 예시 | review_status=draft | N |
| SR-04 | 입력 라벨(text-input) | 사용 환경 조건 | review_status=draft | N |
| SR-04 | 입력 라벨(text-input, P03) | 희망 가격 | review_status=draft | Y |
| SR-04 | 입력 도움말(가격, P03) | 희망 가격을 입력해 주세요. 운영진이 검수할 때 가격도 함께 승인해요. | review_status=draft | N |
| SR-04 | 인라인 오류 | 필수 항목이에요. | review_status=draft | N |
| SR-04 | 인라인 오류(가격) | 가격을 입력해 주세요. | review_status=draft | N |
| SR-04 | 필수 확인 항목 | 개인정보·고객정보·회사기밀이 없는 자료예요. | review_status=draft | N |
| SR-04 | 필수 확인 항목 | 저작권 문제가 없는 자료예요. | review_status=draft | N |
| SR-04 | 재검수 안내(승인 자산 수정, P04) | 수정본만 남기고 다시 검수를 받아요. 다시 승인될 때까지 판매 자산에서 내려가요. | review_status=approved, review_status=draft | N |
| SR-04 | 보조 버튼(button-outline) | 임시저장 | review_status=draft | N |
| SR-04 | 임시저장 완료(ex-toast) | 임시저장했어요. 판매 신청 현황에서 이어서 쓸 수 있어요. | review_status=draft | N |
| SR-04 | CTA | 제출하기 | review_status=draft | N |
| SR-05 | 모달 제목(ex-modal-card) | 판매 신청을 제출할까요? | review_status=draft | N |
| SR-05 | 모달 본문(잠금·철회 불가, P05) | 제출하면 검수가 끝날 때까지 자산을 수정하거나 공개 범위를 바꿀 수 없어요. 제출한 신청은 철회할 수 없어요. | review_status=draft, review_status=pending | N |
| SR-05 | 모달 본문(재고지) | 개인정보·고객정보·회사기밀이나 저작권 문제가 없는지 한 번 더 확인해 주세요. | review_status=draft | N |
| SR-05 | 모달 본문(가격, P03) | 희망 가격 {가격}원 · 운영진 승인 후 확정돼요 | review_status=draft | Y |
| SR-05 | CTA | 제출하기 | review_status=pending | N |
| SR-05 | CTA 로딩 | 제출하고 있어요 | review_status=pending | N |
| SR-05 | 보조 버튼(button-outline) | 돌아가서 수정 | review_status=draft | N |
| SR-06 | 상단 제목 | 판매 신청 현황 | role=seller | N |
| SR-06 | 탭(segmented-control) | 전체 · 임시저장 · 검수 대기 · 수정 요청 · 결과 | review_status=draft, review_status=pending, review_status=revision_requested, review_status=approved, review_status=rejected | N |
| SR-06 | 제출 완료 안내 | 판매 신청을 제출했어요. 검수 결과는 알림으로 알려드려요. | review_status=pending | N |
| SR-06 | 행 보조 문구(임시저장) | 이어서 작성하기 | review_status=draft | N |
| SR-06 | 행 보조 문구(검수 대기) | 운영진이 검수하고 있어요. | review_status=pending | N |
| SR-06 | 행 보조 문구(재검수, P04) | 수정본을 다시 검수하고 있어요. | review_status=pending | N |
| SR-06 | 행 보조 문구(수정 요청) | 수정 요청을 확인해 주세요. | review_status=revision_requested | N |
| SR-06 | 빈 상태 제목(ex-empty-state-card) | 아직 판매 신청한 자산이 없어요 | role=seller | N |
| SR-06 | 빈 상태 버튼(ex-empty-state-card) | 내 자산 보기 | role=seller | N |
| SR-07 | 상단 제목 | 수정 요청이 왔어요 | review_status=revision_requested | N |
| SR-07 | 섹션 라벨 | 운영진 코멘트 | review_status=revision_requested | N |
| SR-07 | 안내 본문 | 코멘트를 반영해 수정한 뒤 다시 제출해 주세요. 다시 제출하기 전까지는 판매 자산이 될 수 없어요. | review_status=revision_requested | N |
| SR-07 | CTA | 수정하러 가기 | review_status=revision_requested | N |
| SR-08 | 상단 제목(승인) | 판매 자산으로 승인됐어요 | review_status=approved | Y |
| SR-08 | 승인 가격 | 승인 가격 {가격}원 | review_status=approved | Y |
| SR-08 | 안내 본문(승인 자산 수정, P04) | 자산을 수정하면 판매 자산에서 내려가고 다시 검수를 받아요. | review_status=approved | N |
| SR-08 | CTA(승인, button-outline) | 내 자산으로 | review_status=approved | N |
| SR-08 | 상단 제목(반려) | 판매 신청이 반려됐어요 | review_status=rejected | N |
| SR-08 | 섹션 라벨 | 반려 사유 | review_status=rejected | N |
| SR-08 | 안내 본문(반려) | 자산을 수정한 뒤 다시 판매 신청할 수 있어요. 공개 범위를 비공개나 멤버 공개로 바꿀 수도 있어요. | review_status=rejected | N |
| SR-08 | CTA(반려, button-outline) | 자산 상세 보기 | review_status=rejected | N |
