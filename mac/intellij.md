인텔리제이, Intellij

# Toolbox 소개 및 프로젝트 생성하기
- 인텔리J를 직접 다운로드하는 것보다 Toolbox App을 설치하고 거기서 인텔리J를 사용하는 것을 추천
- Toolbox는 설정을 앱 안에서 해결할 수 있음 => maximum heap size
- Update to Release(EAP라는 프리뷰때 알람을 할지)

# 메인메소드 생성하고 실행하기
- Find Action : Command shift A
- plugin : presentation assistant

흔히 사용하는 메서드 저장된 것이 있음 => 라이브 템플릿 / 코드 템플릿

RUN : 포커스 실행(control shift R), 
RUN ( control R ) 이전 실행 다시 실행


# 라인 수정하기
한줄 드래그 -> 복사 -> 붙여넣기 과정을 단축키 하나로 해결

- 아래에 동일한 내용 복사 : command D (포커스를 해당 라인에 두고!, 엑셀 기능과 유사하네)
- 해당 줄 내용 삭제 : command + delete
- 라인 합치기 : 하단의 문자열이 합쳐짐(위로 올라옴), control shift j,  SQL Query를 만들 때 자주 사용함
- 라인 옮기기 
    - option shift 위아래 : 문법에 상관없이 이동
    - command shift 위아래 : 이 메소드를 벗어날 수 없음. 파이썬에선  메소드 안이 아니어도 될듯?
- 좌우로 요소 이동 : option shift command 좌우 (html에서 자주 쓰일듯)

# 코드 즉시보기
- 인자값 즉시 보기 : command p 클래스에 들어가서 인자값이 무엇인지 찾기
- 선언부 바로가기 : option space (난 alfred 때문에 안보임)
- docs 미리보기 : f1 (pycharm은 새 창이 뜨네..)

# 포커스 에디터
- 단어별 이동 : option + 화살표
- 이동하며 선택 : option + shift + 화살표
- 라인의 제일 마지막으로 이동 : function + 좌우(command 좌우랑 무슨 차이가 있지?)
- page up/down : function + 위아래

# 포커스 특수키
- Extend selection : option + 위아래  ( 파이참은 작동 안함 )
- 포커스 이전으로 바꾸기 : command + []
- 멀티 포커스 : option 2번(누르고 있는 상태에서) + 방향키
- 오류 포커스 : F2


# 검색 텍스트
- 단어 찾기 : command f
- 단어 수정 : command r
- 프로젝트에서 찾기 : shift command f
- 프로젝트에서 수정 : shift command r
- 찾기에서 정규 표현식 사용 가능


- 최근 열었던 파일 목록 : command e

# 자동 완성
- 스마트 자동 완성 : control shift space


# Live Template
- 포커스에 있는 모든 축약어 나오기 : control j
- command shift a : live template(preference)에 추가 가능

# 리팩토링 - Extract
- option command v : value
- option command p : 파라미터
- option command m : method

# 리팩토링 기타
- 이름 변경 : shift f6
- 타입 변경 : shift command f6
- import 정리 : command option o
    - optimize import on


# 디버깅
- 디버깅 실행 : command shift d









