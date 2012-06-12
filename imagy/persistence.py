from config import PROCESSED_LOC
from tempfile import mktemp
import shelve

processed = seen = originals = None

def init(loc=None):
    global processed, seen, originals
    if loc is None:
        loc = mktemp()
    processed = shelve.open(loc)
    fill(processed)
    seen = processed['set']
    originals = processed['orig']
    return processed

def fill(d):
    for name, typ in (
            ('set', set),
            ('orig', dict),
            ):
        if not name in d:
            d[name] = typ()

def clear(processed):
    processed.clear()
    fill(processed)
    processed.sync()

# provide a persistent dict in a /tmp location by default
# init allows to specify one in a less ephemeral location
processed = init()
