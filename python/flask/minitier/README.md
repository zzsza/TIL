## 미니터 API 시스템
- 미니 트위터

### 핵심 기능
- 회원가입
- 로그인
- 트윗
- 다른 회원 팔로우
- 다른 회원 언팔로우
- 타임라인
- 단, 동시 접속이나 HTTP 요청 처리 속도를 고려한 구현은 하지 않음

### 회원 가입
- 사용자에게 이름, 이메일, 비밀번호 등의 기본 정보를 HTTP 요청을 통해 받은 후 시스템에 저장
- 필요한 정보
    - id
    - name
    - email
    - password
    - profile
    
```
from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.id_count = 1


@app.route("/sign-up", methods=["POST"])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1
    # 실제 구현한다면 atomic_increment operation을 사용해야 함

    return jsonify(new_user)
```

- 아래 코드로 Flask를 실행한 후

```
FLASK_ENV=development FLASK_APP=app.py flask run
```

- httpie로 요청 보내기

```
http -v POST localhost:5000/sign-up name=변성윤 email=zzsza@naver.com password=1234
```

### 300자 제한 트윗 글 올리기
- 사용자는 300자를 초과하지 않는 글을 올릴 수 있음
- 만일 300자를 초과하면 엔드포인트는 400 Bad Request 응답을 보냄
- 사용자가 300자 이내의 글을 전송하면 엔드포인트는 사용자의 글을 저장해야 함 -> 타임라인 엔드포인트를 통해 읽을 수 있ㅇ므
- Tweet 호출시 전송하는 JSON 데이터

```
{
  "id" : 1,
  "tweet" : "My First Tweet"
}
```

- 코드

```
app.tweets = []

@app.route("/tweet", methods=["POST"])
def tweet():
    payload = request.json
    user_id = int(payload["id"])
    tweet = payload["tweet"]
    
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400
        
    if len(tweet) > 300:
        return "300자를 초과했습니다", 400
        
    user_id = int(payload["id"])
    
    app.tweets.append({
        "user_id" : user_id,
        "tweet" : tweet
    })

    return "", 200
```

- 위 코드를 app.py에 넣고 아래 코드로 요청!(id=1이 없다면 오류가 발생함, 현재는 메모리에 데이터 적재)

```
http -v POST localhost:5000/tweet id:=1 tweet="My First Tweet"
```

### 팔로우와 언팔로우
- 팔로우 혹은 언팔로우하고 싶은 사용자의 아이디를 HTTP 요청으로 보내면 API에서 요청을 처리
- 팔로우 엔드포인트에 전송할 JSON 데이터는 아래와 같음
- follow는 팔로우할 사용자의 id

```
{
  "id" : 1,
  "follow" : 2
}
```

- unfollow일 경우는 아래와 같음

```
{
  "id" : 1,
  "unfollow" : 2
}
```

- follow 코드

```
@app.route("/follow", methods=["POST"])
def follow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["follow"])
    
    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400
        
    user = app.users[user_id]
    user.setdefault("follow", set()).add(user_id_to_follow)
    
    return jsonify(user)
```

- `setdefault` : 키가 존재하지 않으면 default 값을 저장하고, 키가 존재하면 해당 값을 읽어들임
- 요청

```
http -v POST localhost:5000/follow id:=1 follow:=2
```

- 에러가 발생하는데, 이 이유는 list는 JSON으로 변경할 수 있지만 set으론 변경하지 못하기 때문
- 이 에러를 위해 CustomJSONEncoder를 구현해 덮어씌워야 함

```
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)
        
app.json_encoder = CustomJSONEncoder
```

- unfollow 코드

```
@app.route("/unfollow", methods=["POST"])
def unfollow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["unfollow"])
    
    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400
        
    user = app.users[user_id]
    user.setdefault("follow", set()).discard(user_id_to_follow)
    
    return jsonify(user)
```

- discard를 사용한 이유 : 삭제하고자 하는 값이 있으면 삭제하고, 없으면 무시하기 때문

### 타임라인 
- 해당 사용자의 트윗들, 팔로우하는 사용자들의 트윗을 리턴
- 데이터 수정 없이 받아오기만 하는 엔드포인트로 HTTP 메소드는 GET
- 리턴하는 JSON 데이터는 아래와 같은 형태

```
{
    "user_id" : 1,
    "timeline" : [
      {
        "user_id" : 2,
        "tweet" : "Hello world"
      },
      {
        "user_id" : 1,
        "tweet" : "My first tweet!"
      }
    ]
}
```

- 코드

```
@app.route("/timeline/<int:user_id>", methods=["GET"])
def timeline(user_id):
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400
    
    follow_list = app.users[user_id].get("follow", set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet["user_id"] in follow_list]
    
    return jsonify({
        "user_id" : user_id,
        "timeline" : timeline
    })
```

- 요청

```
http -v GET localhost:5000/timeline/1
```