from config import PROCESSED_LOC
from tempfile import mktemp
import shelve

class Store(object):
    def __init__(self, loc=None):
        self.load(loc)
    
    @property
    def touched(self):
        return self.d['set']
    
    @property
    def originals(self):
        return self.d['orig']

    def fill():
        for name, typ in (
            ('set', set),
            ('orig', dict),
            ):
            if not name in self.:
                self.d[name] = typ()
    
    def load(self, loc=None):
        if loc == self.loc:
            return
        if loc is None:
            loc = mktemp()
        self.loc = loc
        self.d = shelve.open(loc)
        self.fill()

    def clear(self):
        cleared = len(self.d)
        self.d.clear()
        self.fill()
        self.d.sync()
        
# provide a persistent dict in a /tmp location by default
# init allows to specify one in a less ephemeral location
store = DEFAULTSTORE = Store()
