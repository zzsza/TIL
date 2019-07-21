import logging
from sacred import Experiment

ex = Experiment('log_example')

# set up a custom logger
logger = logging.getLogger('mylogger')
logger.handlers = []
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname).1s] %(name)s >> "%(message)s"')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel('INFO')

ex.logger = logger

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