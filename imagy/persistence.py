from config import PROCESSED_LOC
from tempfile import mktemp
import shelve

def init(loc=None):
    global processed
    if loc is None:
        loc = mktemp()
    processed = shelve.open(loc)
    for name, typ in ((
            'set', set,
            'orig', dict
            )):
        if not name in processed:
            processed[name] = typ()
    return processed

def clear(processed):
    processed.clear()
    return get()

# provide a persistent dict in a /tmp location by default
# but allow to specify one in a less ephemeral
processed = init()
