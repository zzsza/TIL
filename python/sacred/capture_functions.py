from sacred import Experiment
ex = Experiment('my_experiment')


@ex.config
def my_config():
    foo = 42
    bar = 'baz'


@ex.capture
def some_function(a, foo, bar=10):
    print(a, foo, bar)


@ex.automain
def my_main():
    some_function(1, 2, 3)  # 1 2 3
    some_function(1)        # 1 42 'baz'
    some_function(1, bar=12)  # 1 42 12
    some_function()  # TypeError : missing value for 'a'
