# docker 초간단 사용법

- 네이버 AI 해커톤을 하다가 빠르게 도커 사용법을 익혀야 해서, 찾아본 방법
- 추후 기본적인 내용과 함께 블로그에 포스팅 꼭 할 예정입니다
- 기본적인 아이디어는 도커 허브에서 ```docker pull```을 한 후, 수정해서 ```commit```, ```push```



## 기본 명령어
### docker images 
- 현재 사용 가능한 image 목록을 출력. ```-a``` 옵션을 주면 모든 것을 보여줌

### docker rmi <아이디>/<이미지 이름>:<태그>
- 이미지 삭제

### docker ps
- 현재 사용 가능한 컨테이너 목록을 출력. ```-a``` 옵션을 주면 모든 것을 보여줌

### docker pull <아이디>/<이미지 이름>:<태그>
- [docker hub](https://hub.docker.com/)에 있는 이미지를 가지고 옴

### docker 이미지에 접속하고 싶을 경우
- ```docker run -it <아이디>/<이미지 이름>:<태그> /bin/bash```

### docker diff <컨테이너 ID>
- 컨테이너가 부모 이미지와 파일 변경 사항을 확인할 수 있는 명령어

### docker commit <컨테이너 ID> <아이디>/<이미지 이름>:<태그>
- 새로운 도커 이미지 생성

### docker push <아이디>/<이미지 이름>:<태그>
- docker hub에 이미지 업로드

### docker build --tag <아이디>/<이미지 이름>:<태그>
- ```Dockerfile```에 있는 곳에서 명령어를 치면 파일에 나온대로 이미지 생성

### Dockerfile 형식
```
FROM ubuntu:14.04
MAINTAINER Foo Bar <foo@bar.com>

RUN apt-get update
RUN apt-get install -y nginx
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx

WORKDIR /etc/nginx

CMD ["nginx"]
```

- ```FROM``` : 어떤 이미지를 기반으로 할지 설정
- ```MAINTAINER``` : 메인테이너 정보
- ```RUN``` : 쉘 스크립트 혹은 명령 실행
	- 이미지 생성 중에는 사용자 입력을 받을 수 있어서, apt-get install에서 ```-y``` 옵션을 꼭 넣어줘야 함. 안 넣으면 Fail
	- ```RUN```은 한줄이 이미지 하나로 빌드됨
- ```CMD``` : 컨테이너가 시작되엇을 때 실행할 실행 파일 또는 쉘 스크립트
- ```WORKDIR``` : CMD에서 설정한 실행 파일이 실행될 디렉터리 