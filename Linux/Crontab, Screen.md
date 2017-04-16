# Linux

### Screen
```{r, engine='bash', code_block_name} ...
Screen 을 띄워놓고 작업 진행!
- screen --help : 도움말
- screen dmS name : name의 스크린을 생성
- screen -list : 현재 스크린을 보여줌
- screen -r xxxx.kyle(name) -> 접속!! 그 후 exit를 입력하면 세션이 나가짐
- 세션에서 나가지 않고 화면전환은 control + a + d 를 누르면 됨..!
```

### Crontab
```{r, engine='bash', code_block_name} ...
Crontab : 예약 작업을 수행

*   *   *   *   *  수행할 명령어
┬   ┬   ┬   ┬   ┬
│   │   │   │   │
│   │   │   │   │
│   │   │   │   └───────── 요일 (0 - 6) (0 =일요일)
│   │   │   └────────── 월 (1 - 12)
│   │   └─────────── 일 (1 - 31)
│   └──────────── 시 (0 - 23)
└───────────── 분 (0 - 59)


0 8 * * 1-5 /root/weekday.sh : → 평일(월요일~금요일) 08:00 weekday.sh을 실행

```