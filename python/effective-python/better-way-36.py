import subprocess
from time import time
import os

# proc = subprocess.Popen(
#     ['echo', 'Hello from the child!"'],
#     stdout=subprocess.PIPE)
# out, err = proc.communicate()
# print(out.decode("utf-8"))

# proc = subprocess.Popen(["sleep", "0.3"])
# while proc.poll() is None:
#     print("Working...")
#
# print("Exit status', proc.poll()")


def run_sleep(period):
    proc = subprocess.Popen(["sleep", str(period)])
    return proc


start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)


for proc in procs:
    proc.communicate()
end = time()

print("Finished in {:3f} seconds".format(end-start))

#========

proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()


print("Exit status", proc.poll())