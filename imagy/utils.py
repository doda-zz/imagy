from path import path
import filecmp
from tempfile import NamedTemporaryFile
import os
from filecmp import _sig, cmp as same_file

# the mark that is used to identify stored originals that have been modified
MARK = '!'

def make_path(p, sep='_'):
    '''Find a similar, yet unused path'''
    p = path(p)
    name, ext = p.splitext()
    n = 1
    while p.exists():
        p = path('%s%s%s%s' % (name, sep, n, ext))
        n += 1
    return p

def mktemp():
    f = NamedTemporaryFile(delete=False)
    f.close()
    loc = path(f.name).abspath()
    loc.remove()
    return loc

def filesig(pth):
    '''
    a signature of the file, if this remains the same we can be pretty sure that the file hasn't been changed
    '''
    return filecmp._sig(os.stat(pth))

def dump(store):
    '''for debugging purposes'''
    from pprint import pprint
    for p in (store.originals, store.storedat, store.ignored):
        pprint(p)

def callable_or_value(obj):
    if callable(obj):
        return obj()
    return obj

def do(obj, default=None):
    if not config.DRY_RUN:
        return callable_or_value(f)
    return callable_or_value(default)
        
