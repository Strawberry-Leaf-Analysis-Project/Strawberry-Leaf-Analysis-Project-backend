# plants_group

> 유저별 작물 분류 기능의 설명을 적어놓은 문서

## URL별 기능
※ 아래의 기능은 로그인이 되어있어 쿠키로 세션 데이터를 가지고 있다는 전재로 설명함
1. [post] plants_group/ \
기능: 작물그룹 생성 \
필요값: date,name,status \
반환값: 작물그룹 db값(model 인자 전부) 


2. [patch] plants_group/change_status/ \
기능: 작물그룹의 상태값 변경 \
필요값: status \
반환값: 상태 변경이 완료된 작물그룹 db값(model 인자 전부)


3. [patch] plants_group/change_name/ \
기능: 작물그룹의 이름 변경 \
필요값: name \
반환값: 이름 변경이 완료된 작물그룹 db값(model 인자 전부)


4. [get] plants_group/user_list/ \
기능: 사용자의 작물그룹 전체를 반환함 \
필요값: 없음 \
반환값: 사용자의 작물그룹 리스트  
