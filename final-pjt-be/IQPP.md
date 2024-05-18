# Vue 튜토리얼
1. vite 프로젝트 생성  
`$ npm create vue@latest`
2. 프로젝트 설정 관련 절차 진행
![alt text](image.png)
3. 프로젝트 폴더 이동  
`cd <프로젝트 명>`
4. package install  
`npm install`
5. Vue 프로젝트 서버 실행  
`$ npm run dev`

# POSTMAN으로 회원가입 확인할 때
1. POST/ 해당 url 설정
2. Body >> form-data에서 각각 해당하는 key:value값 입력
3. Send 했을 때 204 No Content 뜨면 성공 (db:accounts_user 가서 데이터 저장 확인)
* reference
![alt text](image-1.png)