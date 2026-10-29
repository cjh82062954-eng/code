#mission1 workstation
##1) 실행 환경
- OS : Ubuntu 18.04.2 LTS (WSL2)
- Shell: bash
- Docker: 29.9.2
- Git: 2.17.1

- ## 2) 수행 체크리스트
- [o] 터미널 기본 조작 및 폴더 구성 (`~/mission1/app`)
- [o] 권한 변경 실습 (`chmod 755`, `chmod 644`)
- [o] Docker 설치/점검 (`docker --version`, `docker info`)
- [o] hello-world 실행 및 우분투 컨테이너 테스트
- [o] Dockerfile 빌드/실행 (Nginx 기반 커스텀 웹 서버)
- [o] 포트 매핑 접속 및 검증 (`8080:80`)
- [o] 볼륨 영속성 검증 (`my_work_vol` 데이터 유지 테스트)
- [o] Git 설정 + GitHub 연동 및 푸시 완료 (`main` 브랜치)

  ## 3) 수행 로그(발췌)
  -터미널 기본 조작 및 폴더 구성
   #디렉토리 생성 및 이
   root@DESKTOP-V60E01R:~# mkdir -p ~/mission1/app
   root@DESKTOP-V60E01R:~# cd ~/mission1
   #파일 생성 및 내용 확
   root@DESKTOP-V60E01R:~/mission1# echo "Hello Codyssey Workstation" > app/index.html
   root@DESKTOP-V60E01R:~/mission1# cat app/index.html
   Hello Codyssey Workstation

  -권한 변경 실습
   #권한 실습(파일 및 디렉토리)
   root@DESKTOP-V60E01R:~/mission1# mkdir test_dir
   root@DESKTOP-V60E01R:~/mission1# touch test_file.txt
   #권한 변경 전 확인
   root@DESKTOP-V60E01R:~/mission1# ls -la
   total 16
   drwxr-xr-x 4 root root 4096 Oct 29 22:21 .
   drwx------ 6 root root 4096 Oct 29 22:21 ..
   drwxr-xr-x 2 root root 4096 Oct 29 22:21 app
   drwxr-xr-x 2 root root 4096 Oct 29 22:21 test_dir
   -rw-r--r-- 1 root root    0 Oct 29 22:21 test_file.txt
   #권한 변경 (디렉토리는 755, 파일은 644 설정)
   root@DESKTOP-V60E01R:~/mission1# chmod 755 test_dir
   root@DESKTOP-V60E01R:~/mission1# chmod 644 test_file.txt
   #권한 변경 후 확인 (증거로 남김)
   root@DESKTOP-V60E01R:~/mission1# ls -la
   total 16
   drwxr-xr-x 4 root root 4096 Oct 29 22:21 .
   drwx------ 6 root root 4096 Oct 29 22:21 ..
   drwxr-xr-x 2 root root 4096 Oct 29 22:21 app
   drwxr-xr-x 2 root root 4096 Oct 29 22:21 test_dir
   -rw-r--r-- 1 root root    0 Oct 29 22:21 test_file.txt

  -Docker 설치 및 점검/hello-world 실행
  root@DESKTOP-V60E01R:~/mission1# docker --version
  Docker version 29.9.2, build a82e528
  root@DESKTOP-V60E01R:~/mission1# docker info | grep -E "Operating System|Kernel Version"
  Kernel Version: 6.6.114.1-microsoft-standard-WSL2
  Operating System: Docker Desktop
  root@DESKTOP-V60E01R:~/mission1# docker run hello-world
  Hello from Docker!
  This message shows that your installation appears to be working correctly.

  4.Dockerfile 빌드 및 실행 (Nginx 커스텀 웹 서버)
  #다커 파일 내
  root@DESKTOP-V60E01R:~/mission1# cat << 'EOF' > Dockerfile
  > FROM nginx:alpine
  > LABEL org.opencontainers.image.title="my-custom-nginx"
  > COPY app/ /usr/share/nginx/html/
  > EXPOSE 80
  > EOF
  #빌드 및 실행 로그
  > root@DESKTOP-V60E01R:~/mission1# docker build -t my-web-image:1.0 .
  [+] Building 0.4s (7/7) FINISHED                                                                         docker:default
  => [internal] load build definition from Dockerfile                                                               0.0s
  => => transferring dockerfile: 153B                                                                               0.0s
  => [internal] load metadata for docker.io/library/nginx:alpine                                                    0.0s
  => [internal] load .dockerignore                                                                                  0.0s
  => => transferring context: 2B                                                                                    0.0s
  => [internal] load build context                                                                                  0.0s
  => => transferring context: 211B                                                                                  0.0s
  => [1/2] FROM docker.io/library/nginx:alpine@sha256:a3554c0d0b48177b1413c26e01f695334428020d9df01243fbae3e11cfd1  0.0s
  => => resolve docker.io/library/nginx:alpine@sha256:a3554c0d0b48177b1413c26e01f695334428020d9df01243fbae3e11cfd1  0.0s
  => CACHED [2/2] COPY app/ /usr/share/nginx/html/                                                                  0.0s
  => exporting to image                                                                                             0.2s
  => => exporting layers                                                                                            0.0s
  => => exporting manifest sha256:f46a485d769fd5b43a3704a43a0f5682ea8a3e45e794def192ff161f13390028                  0.0s
  => => exporting config sha256:1a31ffc5b8bb68923629bf24ef6272bede0940fcc8b8f78136175a3b34f529ac                    0.0s
  => => exporting attestation manifest sha256:315cf0bbb7fec70dc6e53c11fee911e172754fdcee060deedc3f6cb140fe60f6      0.0s
  => => exporting manifest list sha256:5168fc210097be4476a67b932362d630d7debf7e2159ad78e046072b3b547a89             0.0s
  => => naming to docker.io/library/my-web-image:1.0                                                                0.0s
  => => unpacking to docker.io/library/my-web-image:1.0                                                             0.0s
 root@DESKTOP-V60E01R:~/mission1# docker run -d -p 8080:80 --name my-web-container my-web-image:1.0
 3bdbb88741bb4f8f5255a5b38704b05e24a1093b9799508a39550f2b724edb97

 5.포트 매핑 접속및검증  
 root@DESKTOP-V60E01R:~/mission1# curl http://localhost:8080
 <!DOCTYPE html>
 <html>
 <head>
 <title>My Workstation Web</title>
 </head>
 <body>
 <h1>Hello from Custom Docker Web Server!</h1>
 </body>
 </html>

 6.불륨 영속성 검증
 root@DESKTOP-V60E01R:~/mission1# docker volume create my_work_vol
 my_work_vol
 root@DESKTOP-V60E01R:~/mission1# docker run -d --name vol-test-container -v my_work_vol:/data ubuntu sleep infinity
 3dbef3770a7b5a6db37e578713537966f7f93c94c7fc0304c927e65124ab9815
 root@DESKTOP-V60E01R:~/mission1# docker exec -it vol-test-container bash -c "echo 'Persistent Data Test' > /data/test.txt"
 root@DESKTOP-V60E01R:~/mission1# docker exec -it vol-test-container cat /data/test.txt
 Persistent Data Test
 root@DESKTOP-V60E01R:~/mission1# docker rm -f vol-test-container
 vol-test-container

 #새로운 컨테이너에 동일 볼륨 연결 후 데이터 생존 확인
 root@DESKTOP-V60E01R:~/mission1# docker run -d --name vol-test-container -v my_work_vol:/data ubuntu sleep infinity
 3dbef3770a7b5a6db37e578713537966f7f93c94c7fc0304c927e65124ab9815
 root@DESKTOP-V60E01R:~/mission1# docker exec -it vol-test-container bash -c "echo 'Persistent Data Test' > /data/test.txt"
 root@DESKTOP-V60E01R:~/mission1# docker exec -it vol-test-container cat /data/test.txt
 Persistent Data Test

 root@DESKTOP-V60E01R:~/mission1# docker rm -f vol-test-container-2
 vol-test-container-2
 root@DESKTOP-V60E01R:~/mission1# docker volume rm my_work_vol
 my_work_vol

7.Git 설정 및 GitHub 연동 / 푸시
root@DESKTOP-V60E01R:~/mission1# git config --global user.name "cjh82062954-eng"
root@DESKTOP-V60E01R:~/mission1# git config --global user.email "***********@gmail.com"
root@DESKTOP-V60E01R:~/mission1# git init
root@DESKTOP-V60E01R:~/mission1# git add .
root@DESKTOP-V60E01R:~/mission1# git commit -m "mission workstation"
root@DESKTOP-V60E01R:~/mission1# git remote add origin https://github.com/cjh82062954-eng/code.git
root@DESKTOP-V60E01R:~/mission1# git pull origin main --allow-unrelated-histories
root@DESKTOP-V60E01R:~/mission1# git push -u origin main
To https://github.com/cjh82062954-eng/code.git
   de55a36..acee258  main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
