# 🚀 미션1 보고서

## 1) 실행 환경
- OS: Windows 11 
- Shell: PowerShell (윈도우 기본 터미널)
- Docker: Docker Desktop (WSL 2 백엔드 연동)
- Git: Git for Windows (버전 관리 도구)

---

## 2) 수행 체크리스트
- [x] 터미널 기본 조작 및 과제 폴더 생성 (`mission1`)
- [x] Docker 설치 및 정상 작동 여부 확인
- [x] 간단한 웹 서버용 `Dockerfile` 및 소스코드 작성
- [x] 도커 이미지 빌드 및 컨테이너 실행
- [x] 포트 매핑을 통해 웹 브라우저로 접속 확인 (2회)
- [x] 바인드 마운트를 통해 파일 수정 시 실시간 반영 확인
- [x] Docker 볼륨을 이용한 데이터 영속성(저장 유지) 검증
- [x] Git 초기화, 사용자 설정, 그리고 깃허브 연동 및 업로드 완료

---

## 3) 주요 수행 과정 및 로그 (발췌)

### (1) 폴더 생성 및 이동
파워셸에서 과제를 진행할 빈 폴더를 만들고 이동한 기록입니다.
\`\`powershell
PS C:\Users\USER> cd C:\Users\USER
PS C:\Users\USER> mkdir mission1
PS C:\Users\USER> cd mission1
\`\`powershell

### (2) 웹 서버용 설정 파일 (`Dockerfile`)
Nginx 가벼운 웹 서버를 기반으로 커스텀 웹페이지를 올리도록 작성했습니다.
\`\`dockerfile
FROM nginx:alpine
COPY app/ /usr/share/nginx/html/
\`\`scripts

### (3) 도커 포트 매핑 실행 (2회 테스트)
내 컴퓨터의 포트(`8080`, `8081`)와 도커 컨테이너 안의 웹 서버(`80`)를 연결하여 실행했습니다.
\`\`powershell
# 첫 번째 접속 테스트 (8080 포트)
PS C:\Users\USER\mission1> docker build -t my-web:1.0 .
PS C:\Users\USER\mission1> docker run -d -p 8080:80 --name web-test1 my-web:1.0
PS C:\Users\USER\mission1> curl http://localhost:8080
Hello! My name is Developer!

# 두 번째 접속 테스트 (8081 포트)
PS C:\Users\USER\mission1> docker run -d -p 8081:80 --name web-test2 my-web:1.0
PS C:\Users\USER\mission1> curl http://localhost:8081
Hello! My name is Developer!
\`\`powershell

### (4) 볼륨 영속성(데이터 보존) 검증 로그
컨테이너를 지웠다 다시 만들어도 데이터가 안전하게 살아있는지 확인한 과정입니다.
\`\`powershell
PS C:\Users\USER\mission1> docker volume create mydata
PS C:\Users\USER\mission1> docker run -d --name vol-test -v mydata:/data nginx alpine sleep infinity
PS C:\Users\USER\mission1> docker exec -it vol-test sh -c "echo 'test data' > /data/hello.txt && cat /data/hello.txt"
test data

# 기존 컨테이너를 삭제한 뒤, 새 컨테이너에 같은 볼륨을 연결해 데이터가 유지되는지 확인
PS C:\Users\USER\mission1> docker rm -f vol-test
PS C:\Users\USER\mission1> docker run -d --name vol-test2 -v mydata:/data nginx alpine sleep infinity
PS C:\Users\USER\mission1> docker exec -it vol-test2 sh -c "cat /data/hello.txt"
test data
PS C:\Users\USER\mission1> docker rm -f vol-test2
\`\`powershell

---

## 4) Git 설정 및 깃허브 업로드
내 컴퓨터에서 작업한 내용을 깃허브 원격 저장소에 안전하게 저장(푸시)했습니다.
\`\`powershell
PS C:\Users\USER\mission1> git config --global user.name "cjh82062954-eng"
PS C:\Users\USER\mission1> git config --global user.email "cjh82062954@naver.com"
PS C:\Users\USER\mission1> git init
PS C:\Users\USER\mission1> git remote add origin https://github.com/cjh82062954-eng/code.git
PS C:\Users\USER\mission1> git add .
PS C:\Users\USER\mission1> git commit -m "feat: complete workstation mission"
PS C:\Users\USER\mission1> git push -u origin main
\`\`powershell

- **제출 저장소 링크:** https://github.com/cjh82062954-eng/code
"@ -Encoding utf8