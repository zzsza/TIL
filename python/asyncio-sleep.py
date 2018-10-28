import asyncio
import time


async def hello_world():
    print("hello world!")


async def hello_python():
    print("hello python!")
    await asyncio.sleep(0.1)

event_loop = asyncio.get_event_loop()
try:
    result = event_loop.run_until_complete(asyncio.gather(
            hello_world(),
            hello_python(),
    ))
    print(result)
finally:
    event_loop.close()

# asyncio.sleep은 time.sleep의 비동기식 구현
# asynci.gather는 await 키워드를 한번만 사용해 코루틴 여러개ㅡㄹ 기다릴 때 사용