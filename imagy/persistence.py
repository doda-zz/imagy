from tempfile import NamedTemporaryFile
import shelve
from path import path

class Store(object):
    def __init__(self, loc=None):
        self.load(loc)
    
    def __getattr__(self, name):
        return getattr(self.d, name)

    def load(self, loc=None):
        if loc is None:
            f = NamedTemporaryFile(delete=False)
            f.close()
            loc = path(f.name)
            loc.remove()
        self.loc = loc
        self.d = shelve.open(loc)

    def clear(self):
        cleared = len(self.d)
        self.d.clear()
        self.d.sync()
        return cleared

    def originals(self):
        return ((k,v) for k,v in self.iteritems() if v != '!')

    def __iter__(self):
        return iter(self.d)

    def __setitem__(self, key, item):
        self.d[key] = item

    def __delitem__(self, key):
        del self.d[key]
        
    def __len__(self):
        return len(self.d)

# provide a persistent dict in a /tmp location by default
# load allows to specify one in a less ephemeral location
store = Store()
