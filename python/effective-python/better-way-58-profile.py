from cProfile import Profile
from pstats import Stats

def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result

def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)


profiler = Profile()
profiler.runcall(test)

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()

# ncalls : 호출 횟수, tottime : 함수 실행되는 소비한 초 단위, tottime percall : tottime을 ncalss로 나눈 값

#       20003 function calls in 1.413 seconds
#
# Ordered by: cumulative time
#
# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#      1    0.000    0.000    1.413    1.413 better-way-58-profile.py:22(<lambda>)
#      1    0.002    0.002    1.413    1.413 better-way-58-profile.py:4(insertion_sort)
#  10000    1.392    0.000    1.410    0.000 better-way-58-profile.py:10(insert_value)
#   9991    0.018    0.000    0.018    0.000 {method 'insert' of 'list' objects}
#      9    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
#      1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
