from sacred import Experiment

ex = Experiment('my_commands')


@ex.config
def cfg():
    name = 'kyle'


@ex.command
def greet(name):
    print('Hello {}! Nice to greet you!'.format(name))


@ex.command
def shout():
    print('WHAZZZUUUUUUUUUUP!!!????')


@ex.automain
def main():
    print('This is just the main command. Try greet or shout.')