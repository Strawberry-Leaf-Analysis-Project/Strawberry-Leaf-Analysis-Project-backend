# Strawberry-Leaf-Analysis-Project-backend

> 딸기 잎 분석 프로젝트의 백엔드 파트
>

산학 연계 프로젝트로 진행하고 있는 딸기 잎에 따른 생장상태 파악 서비스의 백엔드 파트를 담당하는
부분 입니다.

## Using
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">
<img src="https://img.shields.io/badge/Pycharm-000000?style=for-the-badge&logo=Pycharm&logoColor=white">

## 설치 방법

윈도우:

```sh
git clone https://github.com/Strawberry-Leaf-Analysis-Project/Strawberry-Leaf-Analysis-Project-backend.git 
```

## 업데이트 내역

* 0.2.0
  * 추가: 데이터베이스 구조변경에 따른 기능
* 0.1.7
  * 추가: 게시물 수정(제목,내용) 기능
* 0.1.6
  * 수정: 검색기능 쿼리스트링으로 받게끔 수정
* 0.1.5
  * 추가: 게시물 검색 기능
* 0.1.4
  * 추가: 조회수의 무분별한 증가를 방지하는 기능 
* 0.1.3
  * 추가: 비밀번호 저장시 DB에 암호화된 상태로 저장
* 0.1.2
  * 수정: 서비스 시간설정을 UTC->KSF로 변경
  * 수정: rest api 적용을 통해 필요 없어진 코드 및 문서 제거
  * 추가: 게시물 접근시 조회수 증가하는 기능
* 0.1.1
    * 추가: 로그인 기능 1차 구현
      * 상세: 회원가입시 이미지를 저장할 폴더를 유저별로 생성
    * 추가: 게시판 기능 1차 구현
      * 상세: 전체 게시판과 자신이 작성한 게시물만 보이는 `나의 생장일지` 구현
* 0.1.0
    * rest api 적용을 위한 초기 구성 및 코드 변경
* 0.0.1
    * 기능 초안 구성
* 0.0.1
    * 작업 진행 중

## 정보

참여자: shin5774 – babo5774mith@gmail.com

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki