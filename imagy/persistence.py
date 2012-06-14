from config import STORE_LOC
from tempfile import NamedTemporaryFile
import shelve
from path import path

class Store(object):
    def __init__(self, loc=None):
        self.loc = loc
        self.load(loc)
    
    @property
    def touched(self):
        return self.d['set']
    
    @property
    def originals(self):
        return self.d['orig']

    def fill(self):
        for name, typ in (
            ('set', set),
            ('orig', dict),
            ):
            if not name in self.d:
                self.d[name] = typ()
    
    def load(self, loc=None):
        if loc is None:
            f = NamedTemporaryFile(delete=False)
            f.close()
            loc = path(f.name)
            loc.remove()
        self.loc = loc
        self.d = shelve.open(loc)
        self.fill()

    def clear(self):
        cleared = len(self.d)
        self.d.clear()
        self.fill()
        self.d.sync()

    def __getattr__(self, name):
        return getattr(self.d, name)
        
# provide a persistent dict in a /tmp location by default
# load allows to specify one in a less ephemeral location
store = DEFAULTSTORE = Store()
