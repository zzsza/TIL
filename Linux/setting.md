

# setting
- setting은 보통 .bashrc / .bashprofile / .zshrc 등에서 진행
- bashrc는 bash이 실행될 때마다 수행
- .bash_profile은 bash이 login shell로 쓰일 때(즉 처음 login할 때)에 수행.

- child shell은 부모로부터 환경변수를 이어받으니 .bashrc에서 따로 PATH를 설정해 줄 필요는 없지만,  GUI 환경에서 새 terminal을 여는 경우에는 login shell로 처리되지 않으므로 주의가 필요

[참고](http://dogfeet.github.io/articles/2012/bash-profile.html)

## syslog
로그파일 종류

/var/log 디렉토리에 위치

- message : 시스템 운영에 대한 전반적인 기록
- boot.log : 부팅될 때 출력되는 메세지 기록
- cron : cron 기록


## 소유자 변경 (chown)
~~~
chown [변경할 소유자] [변경할 파일]
~~~
- 