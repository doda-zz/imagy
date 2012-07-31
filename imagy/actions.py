'''
Below is an abstraction of actions, this allows greater power in modifying the behavior of the system,
for example in implementing --dry-run without littering the code with:

if not DRY_RUN:
    actually_do_stuff()

instead everything that possibly affects the system is an Action instance that disguises as a callable
so we can have greater control over logging and actual invocation from one place

#separationofconcernswin
'''

from path import path

class Action(object):
    def __init__(self, domsg):
        self.domsg = domsg

    def __call__(self, *args, **kwargs):
        domsg = kwargs.get('domsg')
        if domsg is None:
            domsg = self.domsg
        if domsg:
            self.msg(*args, **kwargs)
        self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        pass

class Move(Action):
    def run(self, pth, pth2):
        path(pth).move(pth2)

move = Move()

move('/home/ddd/a', '/home/ddd/a2')
