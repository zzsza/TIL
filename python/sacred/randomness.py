from sacred import Experiment

ex = Experiment('randomness')


@ex.config
def cfg():
    reverse = False
    numbers = 1


@ex.capture
def do_random_stuff(numbers, _rnd):
    print([_rnd.randint(1, 100) for _ in range(numbers)])


@ex.capture
def do_more_random_stuff(_seed):
    print(_seed)


@ex.automain
def run(reverse):
    if reverse:
        do_more_random_stuff()
        do_random_stuff()
        do_random_stuff()
    else:
        do_random_stuff()
        do_random_stuff()
        do_more_random_stuff()

    do_random_stuff()