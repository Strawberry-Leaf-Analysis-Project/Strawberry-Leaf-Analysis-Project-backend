# Board

> 게시판관련 기능들의 설명을 적어놓은 문서

## URL별 기능

※ 아래의 기능은 로그인이 되어있어 쿠키로 세션 데이터를 가지고 있다는 전재로 설명함

1. [post] board/ \
기능: 게시물 생성 \
필요값: id,password,name,email \
반환값: 사용자 db값(model 인자 전부) \
   (이 url은 만들긴 했지만 우리의 의논상 사용하지는 않는걸로)


2. [delete] board/ \
기능: 게시물 삭제 \
필요값: 없음 \
반환값: 없음  


3. [get] board/{id}/ \
기능: 게시물 조회 기능(정확히는 db 값 반환) \
필요값: 없음 \
반환값: 게시판 db값(model 인자 전부,조회수 +1 되어서),is_like:사용자의 해당 게시물 좋아요 여부(문자),0:안함, 1:함


4. [get] board/personal_board/ \
기능: 로그인되어있는 사용자의 게시판 리스트 반환 \
필요값: 없음 \
반환값: 해당 사용자가 만든 게시판의 리스트  


5. [get] board/like_board/ \
기능: 전체 게시판을 좋아요 순으로 정렬 시킨 리스트를 반환 \
필요값: 없음 \
반환값: 좋아요순으로 정렬된 게시판 리스트 


6. [get] board/view_board/ \
기능: 전체 게시판을 조회순으로 정렬 시킨 리스트를 반환 \
필요값: 없음 \
반환값: 조회순으로 정렬된 게시판 리스트 


7. [get] board/date_board/ \
기능: 전체 게시판을 시간순으로 정렬 시킨 리스트를 반환 \
필요값: 없음 \
반환값: 시간순으로 정렬된 게시판 리스트


8. [get] board/search/ \
기능: 검색한 내용(아이디,제목)이 포함된 게시물 리스트를 반환  \
필요값: search \
반환값: 검색한 내용(아이디,제목)이 포함된 게시물 리스트


9. [patch] board/{id}/change_board/ \
기능: 게시물의 제목과 내용을 변경하는 기능  \
필요값: title,explain \
반환값: 변경이 완료된 게시물의 db값(model 인자 전부)


10. [post] board/input_image/ \
기능: 게시물의 input_image를 넣는 기능  \
필요값: input_image,group_name(그룹 이름) \
반환값: 게시물의 db값(model 인자 전부) =>기대값: input_image만 들어간 db값


11. [post] board/output_image/ \
기능: input_image의 segmentation 결과를 output_image를 넣는 기능  \
필요값: group_name(그룹 이름) \
반환값: 게시물의 db값(model 인자 전부) =>기대값: output_image도 들어간 db값


12. [post] board/write_board/  
기능: 최종적으로 게시물을 작성하며 동시에 이파리 db도 저장하는 기능  \
필요값: title,explain,group_name \
반환값: 게시물의 db값(model 인자 전부)


13. [patch] board/{id}/push_like/ \
기능: 게시물의 좋아요수를 증감시키는 기능  \
필요값: is_pushed:문자,0:증가,1:감소 \
반환값: 좋아요값의 변경이 완료된 게시물의 db값(model 인자 전부)


14. [get] board/group_board_list/ \
기능: 작물별 게시물 검색 기능  \
필요값: name:작물 이름 \
반환값: 작물이름이 일치하는 게시물의 db값(model 인자 전부)
