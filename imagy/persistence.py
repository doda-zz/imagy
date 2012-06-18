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
touched = pickle.load(mkstemp())
originals = pickle.load(mkstemp())

def load(dir):
    global touched, originals
    touched = pickle.load(dir.joinpath('touched.p'))
    originals = pickle.load(dir.joinpath('originals.p'))
    
def clear(dir):
    pass

class Store(object):
    def __init__(self, loc):
        self.load(loc)
        
    def load(self, loc):
        if loc is None:
            self.originals_loc = mktemp()
            self.touched_loc = mktemp()
        self.touched_loc = dir.joinpath('touched.p')
        self.originals_loc = dir.joinpath('originals.p')
        self.touched = pickle.load(self.touched_loc)
        self.originals = pickle.load(self.originals_loc)

    def clear(self):
        self.touched = set()
        self.originals = {}
        pickle.dump(self.
        
    
