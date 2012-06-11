from config import PROCESSED_LOC
import shelve

processed = None
set_up(processed)
if processed is None:
    processed = shelve.open(PROCESSED_LOC)
    print processed

def set_up(d):
    if d is None:
        processed = shelve.open(PROCESSED_LOC)
        and 'set' in d:
        return
    d['set'] = set()
    

def reset(d):
    d.clear()
    set_up(d)

def load(pth):
    global processed
    processed = shelve.open(pth)
