from concurrent import futures
import random


def compute():
    return sum(
        [random.randint(1, 100) for i in range(1000000)])


with futures.ProcessPoolExecutor() as executor:
    futures = [executor.submit(compute) for _ in range(8)]

results = [f.result() for f in futures]

print(f"Results: {results}")

# 내부적으로 multiprocessing.cpu_count 함수를 호출해 사용할 워커를 결정
# 따라서 별도의 max_workers를 설정할 필요 없음
# class ProcessPoolExecutor(_base.Executor):
#     def __init__(self, max_workers=None):
#         ...
#     if max_workers is None:
#         self._max_workers = multiprocessing.cpu_count()
#     else:
#         self._max_workers = max_workers
