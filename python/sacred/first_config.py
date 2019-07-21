from sacred import Experiment
from sacred.observers import FileStorageObserver
ex = Experiment('hello_config')
ex.observers.append(FileStorageObserver.create('my_runs'))

@ex.config
def my_config():
    recipient = "world"
    message = "Hello %s!" % recipient

@ex.capture
def some_function(_log):
    _log.info('Custom Info message!')

@ex.automain
def my_main(message):
    some_function()
    print(message)
