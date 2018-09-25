import time

from futurist import periodics


@periodics.periodic(1)
def every_one(started_at):
    print(f"1: {time.time() - started_at}")


w = periodics.PeriodicWorker([
    (every_one, (time.time(), ), {}),
])


@periodics.periodic(4)
def print_stats():
    print(f"stats {list(w.iter_watchers())}")
    

w.add(print_stats)
w.start()