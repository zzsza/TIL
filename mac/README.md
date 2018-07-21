# 맥북 기본 설정

- 화면 분할 기능 : [Spectacle](https://www.spectacleapp.com/) 다운로드 후 손쉬운 사용에서 권한주면 사용 가능 [참고](http://macnews.tistory.com/3198)
- Alfred : alt + space로 검색 및 유틸리티 열기 가능
- karabiner : 한영전환키를 우측 command로 설정 가능! [참고](http://macnews.tistory.com/5043)
- 맥북 화면보호기 [링크](https://plus.google.com/featuredphotos)
- 키보드-입력소스- Caps Lock키로 abc 입력소스 전환 해제하면 좌측 caps lock은 본래의 기능을 사용하게 됨

- 확인되지 않은 개발자가 배포한 어플을 실행하고 싶은 경우, 보안 및 개인 정보 보호쪽에서 확인없이 열기를 체크하거나 터미널에서 아래와 같이 입력한 후 설치! (다시 키고싶다면 -enable)
~~~
sudo spctl --master-disable
~~~
- 그 후, app market에서 update

### zsh setting
- zsh 설치 [진한이형 블로그](http://hjh5488.tistory.com/2)
- 폰트가 깨지는 경우 [meslo](https://github.com/powerline/fonts/blob/master/Meslo/Meslo%20LG%20M%20DZ%20Regular%20for%20Powerline.otf) 설치 후 설정
- ```open .``` 입력하면 finder 열림

### Database tool
- [Sequel Pro](https://www.sequelpro.com/) : MySQL
- [PSequel](http://www.psequel.com/) : PostgreSQL용이라고 하는데 아직 많이 쓰는진 모르겠음

### iterm2 단축키
- command + d : 우측에 새 화면 추가
- command + shift + d : 하단에 새 화면 추가
- command + t : 새 창 추가
- command + [] : 화면 이동
- command + w : 화면 닫기
- command + q : iterm 종료

### markdown 편집기
- macdown, typora

### Vim 명령어
- [블로그 참고](https://zzsza.github.io/development/2018/07/20/vim-tips/)

### Vim 명령모드시 자동 영문전환
```
brew install cmake
git clone https://github.com/vovkasm/input-source-switcher.git
cd input-source-switcher
mkdir build && cd build
cmake ..
make
make install
```

- ```.vimrc```에 설정 추가

```
if filereadable('/usr/local/lib/libInputSourceSwitcher.dylib')
    autocmd InsertLeave * call libcall('/usr/local/lib/libInputSourceSwitcher.dylib', 'Xkb_Switch_setXkbLayout', 'com.apple.keylayout.ABC')
endif
```