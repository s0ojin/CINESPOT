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
## axios 설치
1. 기 생성된 vue project로 이동(없으면 위 순서대로 생성)
2. `npm install axios`
3. 설치 확인
    * `package.json` 파일 생겼으면 성공!
    ```python
    "dependencies": {
        "axios": "^<version_number>"
    }
    ```

# POSTMAN으로 회원가입 확인할 때
1. POST/ 해당 url 설정
2. Body >> form-data에서 각각 해당하는 key:value값 입력
3. Send 했을 때 204 No Content 뜨면 성공 (db:accounts_user 가서 데이터 저장 확인)
* reference
![alt text](image-1.png)

#### 현재까지 생성한 유저
1. harry/admin1234!
2. Ssafy/ssafy1234!

# TMBD API 연결
#### API key:`7664b301eaabecbd10687d87a3fcdbf2`
#### API Token: `eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NjY0YjMwMWVhYWJlY2JkMTA2ODdkODdhM2ZjZGJmMiIsInN1YiI6IjY2NDhhMjZhMGQ2Y2Q2ZjUwZjJmNzA1ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SKALMlciV5bzicwPKpzwwUGyNBw8loqyFDn5cmFpTGE`

## 영화 데이터 받아와서 .json에 저장하기
1. fetch_and_save_movie_data.py 파일이 있는 경로로 이동
2. `python fetch_and_save_movie_data.py` 커맨드 입력
3. 끝!
* 받아오고자 하는 Model이 변경될 때마다 아래 과정 필수
    1. python manage.py makemigratons
    2. python manage.py migrate
 
### TMDB에서 영화 촬영지 정보 받아오려면 credit_id 필요?