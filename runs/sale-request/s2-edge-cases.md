# 엣지케이스 목록 — sale-request

| ID | 상황 | 관련 상태값 | 처리 | 화면 추가 필요(Y/N) | 근거 |
|---|---|---|---|---|---|
| E01 | 판매 승인 전 유료 회원이 SR-03 공개 범위에서 판매 신청(sale_requested)을 선택하려고 함 | role=paid, visibility=sale_requested | SR-03에서 판매 신청 항목을 비활성으로 노출하고, 선택 시 ex-toast로 "판매 신청은 운영진 승인을 받은 회원만 할 수 있어요. 승인 요청은 기존 채널로 해주세요" 안내. 비공개·멤버 공개만 저장 가능 | N | 6-5, 7-3, 7-4, 9 |
| E02 | 판매 승인 전 유료 회원이 알림·공유 링크 등으로 SR-04 판매 신청 정보 입력 화면에 직접 진입 | role=paid, visibility=sale_requested, review_status=draft | SR-04 진입을 차단하고 SR-02 내 자산 상세로 돌려보내며 E01과 같은 안내 ex-toast 노출. draft 생성하지 않음 | N | 7-3, 7-4, 9 |
| E03 | 판매 승인 회원이 검수 대기 중 유료 회원으로 역할이 바뀜(운영자 수동 변경) | role=paid, visibility=sale_requested, review_status=pending | 새 판매 신청은 E01처럼 막고, 진행 중 신청의 상태는 SR-01 badge-overlay로만 읽기 전용 표시. 기존 pending 신청의 유지·취소 여부는 S4 정책 확인 대상 | N | 6-5, 6-7, 7-4 |
| E04 | 판매 신청 자산에 개인정보·고객정보(실명, 연락처, 고객사 데이터 등)가 포함됨 | role=seller, visibility=sale_requested, review_status=pending | SR-04에서 제출 전 "개인정보·고객정보·회사기밀이 없는지" 확인 항목을 필수 체크로 두고, SR-05 확인 모달에서 한 번 더 고지. 검수에서 발견되면 revision_requested로 SR-07에 삭제 요청 코멘트 노출, 재제출 전까지 판매 불가 | N | 6-7, 7-4, 8 |
| E05 | 판매 신청 자산에 회사기밀(사내 문서, 내부 프로세스, 사내 코드)이 포함됨 | role=seller, visibility=sale_requested, review_status=revision_requested | E04와 같은 제출 전 확인. 검수에서 제거 가능하면 revision_requested로 SR-07 안내, 자산 자체가 기밀이면 rejected로 SR-08에 사유 표시 | N | 6-7, 8 |
| E06 | 판매 신청 자산에 저작권 문제가 있는 자료(타인 강의 자료, 유료 템플릿 재배포 등)가 포함됨 | role=seller, visibility=sale_requested, review_status=rejected | SR-04에 "저작권 문제가 없는 자료인지" 필수 확인 항목. 검수에서 발견되면 rejected 처리되어 SR-08에 반려 사유 표시, SR-02로 이동해 공개 범위를 비공개로 되돌릴 수 있음 | N | 6-7, 6-8, 8 |
| E07 | SR-04에서 사용 방법·결과 예시·사용 환경 조건 등 판매 기준 필수 항목이 비어 있는 채로 제출 시도 | role=seller, review_status=draft | text-input 인라인 오류로 빈 항목 표시, 제출 button-primary 비활성. 임시저장은 허용(draft 유지) | N | 6-7, 8 |
| E08 | 임시저장(draft) 후 이탈했다가 다시 들어옴 | role=seller, visibility=sale_requested, review_status=draft | SR-06에서 draft 배지 선택 시 SR-04로 이어 쓰기, 입력값 복원 | N | 6-5, 8 |
| E09 | SR-05에서 제출 버튼을 연속으로 눌러 중복 제출 | role=seller, review_status=pending | 첫 탭 직후 버튼 비활성·로딩 처리, 신청 1건만 pending으로 생성 | N | 6-5, 8 |
| E10 | 검수 대기(pending) 중 자산 내용을 수정하거나 공개 범위를 바꾸려 함 | role=seller, visibility=sale_requested, review_status=pending | SR-02 편집 버튼과 SR-03 공개 범위 선택을 잠그고 ex-toast로 "검수 중에는 수정할 수 없어요" 안내. 신청 철회 기능은 PRD에 없어 제공하지 않음(S4 확인 대상) | N | 6-5, 6-7 |
| E11 | 수정 요청(revision_requested)을 받은 뒤 수정해 재제출 | role=seller, review_status=revision_requested | SR-07에서 운영자 코멘트 확인 후 SR-04로 이동, 기존 입력값 유지한 채 수정, SR-05 제출 시 pending으로 전환. 상태 변경 알림 발송 | N | 6-5, 6-7, 6-8 |
| E12 | 반려(rejected)된 자산을 다시 판매 신청하려 함 | role=seller, visibility=sale_requested, review_status=rejected | SR-08에서 반려 사유 확인 후 SR-02로 이동. 공개 범위는 비공개·멤버 공개로 변경 가능. 같은 자산 재신청 허용 여부는 PRD에 없어 S4 확인 대상 | N | 6-5, 6-7 |
| E13 | 승인됨(approved) 자산의 파일·설명을 판매 승인 회원이 수정하려 함 | role=seller, visibility=sale_requested, review_status=approved | SR-02 편집 시 "수정하면 다시 검수를 받아야 해요" 안내 후 SR-04로 이동, 수정본은 draft로 저장되고 재제출 시 pending. 승인본 유지 방식은 S4 확인 대상 | N | 6-5, 9 |
| E14 | 멤버 공개(member_only) 자산을 판매 신청으로 전환 | role=seller, visibility=member_only, review_status=draft | SR-03에서 판매 신청 선택 시 SR-04로 이동. 전환 후 기존 멤버 열람 유지 여부를 SR-03 안내 문구로 고지(정책은 S4 확인 대상) | N | 6-5, 7-3, 7-4 |
| E15 | 등록된 자산이 하나도 없음 | role=seller, visibility=private | SR-01에 ex-empty-state-card로 "아직 등록한 자산이 없어요" 표시, button-primary로 내 자산 등록 플로우 연결 | N | 6-5 |
| E16 | 판매 신청 내역이 하나도 없는 판매 승인 회원이 상태 확인 화면 진입 | role=seller, review_status=draft | SR-06에 ex-empty-state-card로 빈 상태 안내, SR-01로 연결 | N | 6-5, 7-4 |
| E17 | 비회원·무료 회원이 내 자산 화면(SR-01)에 진입 | role=guest, role=free | 비회원은 로그인 유도, 무료 회원은 유료 멤버십 안내로 연결. 판매 신청 화면 노출 없음 | N | 7-1, 7-2, 7-3 |
| E18 | 상태 변경 알림을 눌러 진입했지만 그 사이 상태가 다시 바뀜(예: 수정 요청 알림 확인 전에 재제출해 pending) | role=seller, review_status=revision_requested, review_status=pending | 알림 딥링크는 최신 review_status 기준 화면(SR-06)으로 열고 현재 배지 표시 | N | 6-8, 8 |
