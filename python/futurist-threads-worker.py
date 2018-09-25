import futurist
from futurist import waiters, rejection
import random


def compute():
    return sum(
        [random.randint(1, 100) for i in range(10000)]
    )


with futurist.ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(compute) for _ in range(8)]
    print(executor.statistics)


results = waiters.wait_for_all(futures)
print(executor.statistics)

print(f"Results: {[r.result() for r in results.done]}")