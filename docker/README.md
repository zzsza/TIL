# docker 초간단 사용법

- 네이버 AI 해커톤을 하다가 빠르게 도커 사용법을 익혀야 해서, 찾아본 방법
- 추후 기본적인 내용과 함께 블로그에 포스팅 꼭 할 예정입니다
- 기본적인 아이디어는 도커 허브에서 ```docker pull```을 한 후, 수정해서 ```commit```, ```push```
- 추가적으로 IBM developerWorks 밋업을 듣고 정리한 내용까지 작성했습니다

# Contents
- [Docker](#docker)
- [Kubernetes](#kubernetes)

# Docker
- Docker : 컨테이너 기반의 오픈소스 가상화 플랫폼
- Images : 컨테이너 실행에 필요한 파일과 설정값 등을 포함하는 것으로, 상태값을 가지지 않고 변하지 않습니다(Immutalble)
	- tar 파일을 묶어놓은 file system으로 Template같은 친구들
- Container : 이미지를 실행한 상태이며 추가되거나 변하는 값은 컨테이너에 저장됩니다
	- 단, 컨테이너를 삭제하면 내부의 데이터가 삭제됩니다. 이를 해결하기 위해 ```Volumn```을 사용합니다 
- [서비큐라님 블로그](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html) : 꼭 읽어보기!! 추천!!!
- [IBM Document](http://docker-dwmeetup.mybluemix.net/docker1.html)

## 기본 명령어
```docker run hello-world```, ```docker container run hello-world``` : 기존에 명령어를 전자같이 사용했으나, 17년 초중반부터 명령어가 후자같이 세분화되고 있습니다

### docker images 
- 현재 사용 가능한 image 목록을 출력. ```-a``` 옵션을 주면 모든 것을 보여줌

### docker rmi <아이디>/<이미지 이름>:<태그>
- 이미지 삭제

### docker ps
- 현재 사용 가능한 컨테이너 목록을 출력. ```-a``` 옵션을 주면 모든 것을 보여줌

### docker pull <아이디>/<이미지 이름>:<태그>
- [docker hub](https://hub.docker.com/)에 있는 이미지를 가지고 옴

### docker 이미지로 container 실행하고 싶은 경우
- ```docker run -it <아이디>/<이미지 이름>:<태그> /bin/bash``` : ```-it``` 옵션과 함께 실행하면 실행한 명령이 Console에 붙어서 진행됩니다. i는 interactive, t는 tty를 의미합니다
- ```docker container run <container 이름> ls -l``` : ls -l 명령어를 실행하며 컨테이너를 실행해라!
- ```docker container run -it --name <container 별명> <image 이름> /bin/ash``` : ```--name```을 통해 container 이름을 부여합니다. container 이름을 부여하지 않으면 랜덤하게 생성됩니다

### exit된 docker container 접속
- ```docker container start <container ID>``` 

### docker container에서 명령어 실행
- ```docker container exec <container ID> ls``` : ```exec```은 container에서 명령어를 실행! ```exec```로 실행하면 ```ps auxf```에 살아있습니다

### docker diff <container ID>
- 컨테이너가 부모 이미지와 파일 변경 사항을 확인할 수 있는 명령어

### docker commit <container ID> <아이디>/<이미지 이름>:<태그>
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
EXPOSE 8080 

WORKDIR /etc/nginx

CMD ["nginx"]
COPY app.js
```

- ```FROM``` : 어떤 이미지를 기반으로 할지 설정
- ```MAINTAINER``` : 메인테이너 정보
- ```RUN``` : 쉘 스크립트 혹은 명령 실행
	- 이미지 생성 중에는 사용자 입력을 받을 수 있어서, apt-get install에서 ```-y``` 옵션을 꼭 넣어줘야 함. 안 넣으면 Fail
	- ```RUN```은 한줄이 이미지 하나로 빌드됨
- ```EXPOSE``` : 포트 노출
- ```CMD``` : 컨테이너가 시작되었을 때 실행할 실행 파일 또는 쉘 스크립트
- ```WORKDIR``` : CMD에서 설정한 실행 파일이 실행될 디렉터리 
- ```COPYT``` : 말 그대로 복사

### Docker Container Stop
- ```docker container rm <container ID/Name>``` : container 삭제! 돌아가고 있는 container는 삭제가 되지 않습니다. 먼저 중지한 후, 삭제해야 합니다! 그러나 ```-f``` 조건을 주면 바로 삭제할 수 있습니다

### Delete all containers
- ```docker rm $(docker container ls -a -q)```
- ```docker container ls -a -q```는 container의 id만 출력합니다

### Delete all images
- ```docker rmi $(docker images -q)```
- ```docker image ls -q | xargs docker image rm``` : docker image들을 삭제! ```xargs```는 앞의 결과를 인자로 받습니다

## Install Docker
```
sudo apt update
sudo apt install -y apt-transport-https ca-certificates software-properties-common curl
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# docker를 다운로드 
sudo apt update
sudo apt install -y docker-ce
id
sudo usermod -a -G docker ibmcloud
# usermod로 등록
id
sudo systemctl restart ttyd
exit
```

## Docker port and volume
- 순서대로 따라해보면 됩니다!
- ```docker container run -d --name mynginx nginx``` : ```-d``` 조건을 줘서 데몬으로 실행
- ```docker containers ls``` : 현재 PORT가 나옵니다!
- ```docker container exec mynginx hostname -I``` : hostname-IP 출력하면 여러 IP가 나옵니다
- ```ifconfig docker0``` : docker가 네트워크도 격리된 환경을 만들었습니다!! IP가 유사하면 서로 접근할 수 있습니다
- ```curl http://<container IP>``` 하면 접근을 한 것을 알 수 있습니다
- ```docker container run -d --name mynginx2 -p 8080:80 nginx:alpine``` : alpine 리눅스 기반으로 호스트의 8080 포트를 컨테이너의 80으로 설정합니다
- ```docker container ls```를 하면 PORTS에 0.0.0.0:8080->80/tcp가 나타납니다! 컨테이너 안에있던 친구들이 외부로 노출된 것을 알 수 있습니다!
- ```cd ~/workspace```한 후, ```docker container cp mynginx2:/etc/nginx/conf.d/default.conf .``` 를 하면 컨테이너 안에 있던 친구들을 호스트로 꺼내왔습니다! 파일에 location을 보면 root : /usr/share/nginx/html이라고 나와있습니다
- ```echo "hello world!" > index.html```을 하신 후, ```docker container cp index.html mynginx2:/usr/share/nginx/html/index.html``` 하면 파일이 바뀜을 알 수 있습니다
- ```docker container run -d --name mynginx3 -p 8083:80 -v /home/ibmcloud/workspace:/usr/share/nginx/html nginx:alpine``` : workspace 디렉토리를 연결해서 실행해보니 8083도 위에서 만든 8080가 동일합니다! 여기서 ```-v``` 옵션을 줘서 다양하게 디렉터리를 공유할 수 있습니다!
- ```docker system prune``` : 멈춰있는 container를 모두 지우고, 태그안된 image 등을 깔끔하게 삭제합니다

## Build Docker image
```
git clone https://github.com/IBM/container-service-getting-started-wt
cd container-service-getting-started-wt/Lab\ 1
cat package.json
cat app.js
cat Dockerfile
```

- ```Dockerfile```은 이미지를 만드는 방법을 나타냅니다  

```
EXPOSE 8080 # 8080 포트 노출
CMD node app.js # app.js 실행!
COPY app.js
```

- ```app.js```를 마지막으로 하면 빌드 과정에서 달라집니다!(COPY package.json 같은 것들이 app.js에 종속됨) 이미지의 순서가 정말 중요합니다
- ```docker image build -t hello-world:1 .``` : docker 빌드
- ```docker image inspect hello-world:1``` : 도커 이미지를 검사합니다
- ```docker container run -d -p 8080:8080 --name hello-world-a hello-world:1``` : 방금 만든 이미지를 사용해 container를 실행합니다
- ```docker container logs <container name>``` : 로그를 확인할 수 있습니다!
- ```docker container exec hello-world-a hostname ip addr |grep inet``` , ```docker container exec hello-world-b hostname ip addr |grep inet``` 해보면 각자의 Network가 생성되어 있습니다! 
- ```docker container stop hello-world-a hello-world-b``` : c를 제외하고 삭제합니다
- ```ps auxf |grep app.js |grep node```해서 process 번호를 확인하고 ```sudo kill <PID>```를 하면 컨테이너가 종료됩니다. c는 kill signal을 주고 로그가 남습니다! 이 죽은 애들을 살려주는 곳이 쿠버네티스!


# Kubernetes
- 앱을 만들면 Container로 실행합니다. 이걸 쿠버네티스에서 ```pod``` (포드, 팟)이라고 부릅니다. 각각의 pod는 1개의 IP를 가집니다! 모이면 리플리카셋이 되고, 이것들을 deployment라고 배포합니다. 이런 친구들은 워커 노드에서 돌아갑니다. 
	- Master Node : 스케쥴링
	- Worker Node : 실제 일을 하는 친구들
- 쿠버네티스는 마스터를 다 관리해줍니다! 요새 IBM, GCP 등에 마스터를 알아서 관리해주고 워커만 저희가 보면 됩니다

## 쿠버네티스의 장점
- 스케쥴링을 잘해줌
- 죽어도 스스로 잘 살려줌
- 확장성
- 로드 밸런싱
- 롤아웃/롤백이 자동으로 진행
- 설정을 관리

## Install kubectl cli
```
sudo apt update && sudo apt install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" |sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubectl
```

- kubectl을 설치해야 합니다!(단 처음 설치하면 tab이 안됨)
- ```kubectl version``` : 쿠버네티스 버전 명시(처음엔 Client만 나올겁니다)
- ```source <(kubectl completion bash)``` : 자동완성 가능하도록 설정
- ```kubectl completion bash |sudo tee /etc/bash_completion.d/kubectl``` : 종료해도 자동완성 가능하도록 설정!


## Deploying apps into clusters
- [문서](http://docker-dwmeetup.mybluemix.net/k8s1.html)

- ```bx login``` : ```au-syd``` 선택!   
- ```bx cr region-set``` : 개인 저장소를 사용하기 위한 명령어. container repository의 약자( ```cs```) ```ap-south``` 선택!  
- ```bx cr namespace-list``` : 이름을 출력!  
- ```export MY_REGISTRY_NAMESPACE=<namespace>``` : 환경설정 추가
- ```bx cr namespace-add $MY_REGISTRY_NAMESPACE``` : 네임스페이스 추가!!
- ```bx cr login``` : ```cat ~/.docker/config.json```을 사용해 로그인합니다
- ```docker image ls``` : 현재 로컬에 있는 docker 이미지 출력
- ```docker image tag hello-world:1 registry.au-syd.bluemix.net/$MY_REGISTRY_NAMESPACE/hello-world:1``` : 같은 Image ID를 가지는 image가 생성됩니다
- ```docker image push registry.au-syd.bluemix.net/$MY_REGISTRY_NAMESPAC/hello-world:1``` : 이미지가 IBM 개인 저장소로 push!
- ```bx cr image-list``` : 개인 저장소에 있는 image를 출력합니다


```
docker image tag hello-world:2 registry.au-syd.bluemix.net/$MY_REGISTRY_NAMESPACE/hello-world:2
docker image push registry.au-syd.bluemix.net/$MY_REGISTRY_NAMESPAC/hello-world:2
``` 
hello-world:2도 올려줍니다!


- ```bx cs clusters``` : 명령어가 ```cs```로 바뀌었습니다! container service
- ```export MY_CLUSTER_NAME=<cluster 이름>```
- ```bx cs workers $MY_CLUSTER_NAME``` : worker들의 설정을 보여줍니다
- ```bx cs cluster-config $MY_CLUSTER_NAME``` : export KUBECONFIG ~를 그대로 복사해서 터미널에서 실행! 해당 config에 쿠버네티스 정보가 나타납니다
- ```kubectl version``` : 이제 Server도 출력됩니다!
- ```kubectl version --short``` : 짧게 Version 출력


### Worker 올리는 부분
- ```kubectl run hello-world-deployment --image=registry.au-syd.bluemix.net/$MY_REGISTRY_NAMESPACE/hello-world:1``` : 해당 image를 가지고 와서 쿠버네티스 실행!
- ```kubectl get pod``` : pod 생성되었는지 확인
- ```kubectl get deployment``` : 방금 deploy한 친구의 정보가 나옵니다. deployment 뒤에 이름을 붙여서 볼수도 있음
- ```kubectl get deployment hello-world-deployment -o yaml``` : ```-o yaml```을 사용해 더 상세한 데이터를 보여줍니다
	- replicas : 1개로 되어있음
	- rollingUpdate : deployment 정책! 1개씩만 올리고 내림
- ```kubectl describe deployment hello-world-deployment``` : 현재 상태를 보여줍니다
- ```kubectl get replicaset``` : replicaset이 나타납니다
- ```kubectl get replicaset -o yaml``` : 특정 replicaset 정보를 가지고 옵니다(여기서 pod 관리 정책이 있음)
- ```kubectl get pod``` : pod이 생겼습니다!!
- ```kubectl get pod -o yaml``` : pod은 특정 ip를 가지고 있습니다! hostIP도 나타나며 다른 정보들도 포함되어 있습니다
	
### pod 외부에서 확인하고 싶을 경우	
- 외부에서 확인하기 위해선 cluster ip, node port 열어주기 등의 방법이 필요합니다. 여기선 node port를 열어보겠습니다
- ```kubectl expose deployment/hello-world-deployment --type=NodePort --port=8080 --name=hello-world-service --target-port=8080
``` 
- ```kubectl describe service hello-world-service``` : 해당 서비스 설명 출력됩니다. 8080:30384/TCP가 되어있습니다!
- ```bx cs workers $MY_CLUSTER_NAME``` : 해당 IP를 확인한 후, nodePORT를 연결하면 접속이 됩니다!
- ```kubectl edit deployment hello-world-deployment``` : deployment를 수정합니다! replicas의 수를 수정할 수 있습니다
- ```kubectl scale --replicas=5 deployment hello-world-deployment``` : replicas 개수를 조절할 수 있습니다
- ```kubectl get pod``` : 하면 개수가 증가됨을 볼 수 있습니다
- ```kubectl rollout status deployment hello-world-deployment``` : rollout 상태를 보여줍니다
- ```kubectl describe replicaset```를 입력하면 4개가 추가됨을 볼 수 있습니다
- ```watch -n 1 curl http://워커아이피:노드포트/``` : 1초마다 해당 내용이 가져오는데, 어떤 팟을 쓰는지 볼 수 있습니다


### Version 오류 발생시 대처가 어떻게 되는지?
- ```export MY_REGISTRY_NAMESPACE=<ID>```
- ```kubectl set image deployment hello-world-deployment hello-world-deployment=registry.au-syd.bluemix.net/$MY_REGISTRY_NAMESPACE/hello-world:3``` : 아직 3을 안만들었지만 생성됨
- ```kubectl rollout status deployment hello-world-deployment``` : 2개가 업데이트되고 진행이 안됩니다
- ```kubectl describe pod``` : 상태가 다릅니다
- ```kubectl get pod``` : 이미지를 PULL하다 에러가 뜸!
- ```kubectl rollout undo deployment hello-world-deployment``` : 롤백!!!!!
- ```kubectl get pod``` : 멀쩡한 것을 볼 수 있습니다


## Reference
- [서비큐라님 블로그](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html) 
- [도커 튜토리얼 : 깐 김에 배포까지](http://blog.nacyot.com/articles/2014-01-27-easy-deploy-with-docker/)
- [Docker에서 apt-get update가 실패할 때](http://interp.blog/docker%EC%97%90%EC%84%9C-apt-get-update%EA%B0%80-%EC%8B%A4%ED%8C%A8%ED%95%A0-%EB%95%8C/)
- [Docker 컨테이너 이미지 생성](http://forum.falinux.com/zbxe/index.php?document_srl=806457&mid=lecture_tip)
- [Image doe not contain 'sudo'](https://github.com/tianon/docker-brew-ubuntu-core/issues/48)
- [developerWorks 밋업, 도커와 쿠버네티스, 두 마리 토끼를 잡자!](https://www.facebook.com/groups/developerWorksKRUG/permalink/2020459798166854/)
- [IBM Document](http://docker-dwmeetup.mybluemix.net/docker1.html)
