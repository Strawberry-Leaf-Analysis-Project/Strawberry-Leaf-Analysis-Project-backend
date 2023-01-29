# Member

> 유저관련 기능들의 설명을 적어놓은 문서

## URL별 기능

1. [post] member/ \
기능: 사용자 회원가입 \
필요값: id,password,name,email \
반환값: 사용자 db값(model 인자 전부) 


2. [get] member/consist_userList/ \
기능: 현재 존재하는 사용자리스트 반환(삭제x상태) \
필요값: x \
반환값: 삭제처리가 안된 전 사용자 리스트 


3. [patch] member/{id}/change_password/
기능: 사용자 비밀번호 변경 \
필요값: password,apassword \
반환값: 사용자 db값(model 인자 전부) 


4. [patch] member/{id}/change_name/ \
기능: 사용자 이름 변경 \
필요값: name \
반환값: 사용자 db값(model 인자 전부)  


5. [post] member/login/
기능: 로그인
필요값: id,password
반환값: message,id,name 


6. [post] member/logout/
기능: 로그아웃
필요상태:로그인상태(캐시데이터가 필요)
반환값: 없음 


7. [post] member/password_check/
기능: 입력값 2개가 일치하는지 확인
필요값: password,check_password
반환값: flag,message


