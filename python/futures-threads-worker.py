# 사용 방법
# 실행자(executor) 선택
# 실행자 : 스케줄링과 비동기 작업을 실행할 책임, 엔진
# 스레드 기반, 프로세스 기반
# Future 객체 : 해당 작업이 미래에 언젠가 완료될 것이라는 일종의 약속

from concurrent import futures
import random


def compute():
    return sum(
        [random.randint(1, 100) for i in range(1000000)])


with futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(compute) for _ in range(8)]

results = [f.result() for f in futures]

print(f"Results: {results}")

# 함수형 프로그래밍 형태
# Future 객체는 done()이나 add_done_callback(fn) 등의 함수도 제공
