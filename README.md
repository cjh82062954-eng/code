# 🚀 개발 워크스테이션 구축 및 Docker/Git 검증 결과보고서

## 1. 제출 저장소 (GitHub Repository)
- **저장소 링크:** [https://github.com/cjh82062954-eng/code.git](https://github.com/cjh82062954-eng/code.git)
- 저장소 권한: Public (공개) 설정 완료, 링크를 통해 전체 산출물 확인 가능

---

## 2. 실행 환경
- **OS:** Windows 10 / 11
- **Terminal / Shell:** PowerShell
- **Docker Version:** Docker Desktop (WSL 2 백엔드 연동)
- **Git Version:** 최신 Git for Windows 설치 및 설정 완료

---

## 3. 수행 항목 체크리스트
- [x] 터미널 및 권한 세팅 (PowerShell 환경)
- [x] Docker Desktop 설치 및 WSL 2 백엔드 연동 확인
- [x] Dockerfile 및 웹 서버 소스코드 작성 (BOM 없는 UTF-8 인코딩)
- [x] 포트 매핑(8080:80)을 통한 웹 서버 컨테이너 구동 및 브라우저 접속 확인
- [x] 바인드 마운트 및 Docker 볼륨 영속성 검증
- [x] Git 사용자 정보 및 기본 브랜치(main) 설정
- [x] GitHub 원격 저장소 연동 및 푸시 완료

---

## 4. 터미널 조작 및 Docker 운영/검증 로그

### (1) 시스템 및 Docker 점검
\\\powershell
docker --version
docker info
\\\

### (2) 웹 서버 빌드 및 컨테이너 실행
\\\powershell
# 이미지 빌드
docker build -t my-web:1.0 .

# 포트 매핑 실행 (8080:80)
docker run -d -p 8080:80 --name web-test my-web:1.0
\\\

### (3) Docker 운영 명령 실행 흔적
\\\powershell
# 1. 이미지 목록 확인
docker images

# 2. 컨테이너 전체 목록 확인
docker ps -a

# 3. 컨테이너 로그 확인
docker logs web-test

# 4. 컨테이너 자원 사용량 모니터링
docker stats --no-stream
\\\

---

## 5. Dockerfile 기반 웹 서버 컨테이너 구조

### (1) 프로젝트 디렉토리 구조
\\\	ext
mission1/
├── app/
│   └── index.html
├── Dockerfile
└── README.md
\\\

### (2) 소스코드 (pp/index.html)
\\html
<html>
  <body>
    <h1>Hello! My name is Developer!</h1>
  </body>
</html>
\\\

### (3) Dockerfile
\\dockerfile
FROM nginx:alpine
COPY app/ /usr/share/nginx/html/
\\\

---

## 6. 포트 매핑 및 브라우저 접속 증거
- **실행 명령:** docker run -d -p 8080:80 --name web-test my-web:1.0
- **접속 주소:** http://localhost:8080
- **확인 결과:** 브라우저 주소창에 위 주소 입력 시 Hello! My name is Developer! 화면 정상 출력 확인

---

## 7. 바인드 마운트 및 Docker 볼륨 검증

### (1) 바인드 마운트 반영 검증
- 호스트의 소스코드 수정 사항이 컨테이너에 즉시 반영되는 구조 구축 완료

### (2) Docker 볼륨 영속성 검증
- 볼륨 생성 및 마운트 연결 명령 수행 후 컨테이너 삭제/재생성 시에도 데이터가 안전하게 유지됨을 확인

---

## 8. 트러블슈팅 (Troubleshooting)

### 트러블슈팅 1: Docker 빌드 중 RST_STREAM 에러 발생
- **문제 발생:** docker build 실행 도중 Internal: stream terminated by RST_STREAM 에러 발생
- **원인 가설:** Windows WSL 2 백엔드와 Docker BuildKit 간의 통신 불안정 또는 버그
- **확인 과정:** 레거시 빌더 모드로 전환하여 빌드 테스트 진행
- **해결/대안:** BuildKit 환경 변수 조정 및 빌드 재시도를 통해 정상 빌드 성공

### 트러블슈팅 2: Dockerfile 파싱 에러 발생
- **문제 발생:** 빌드 시 unknown instruction 계열의 파싱 에러 발생
- **원인 가설:** Windows 편집기 사용으로 인해 파일 상단에 BOM(Byte Order Mark) 헤더가 포함됨
- **확인 과정:** PowerShell 명령어를 통해 인코딩 방식을 확인
- **해결/대안:** Set-Content -Encoding utf8 옵션을 사용하여 BOM 없는 순수 UTF-8 형식으로 파일 재생성 후 해결

---

## 9. Git 설정 및 GitHub 연동 증거
- **Git 사용자 설정:** git config --global user.name 및 user.email 설정 완료
- **원격 저장소 연동:** git remote add origin https://github.com/cjh82062954-eng/code.git
- **최종 푸시 완료:** git push -u origin main을 통해 모든 코드 및 문서 업로드 완료
