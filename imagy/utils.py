from path import path
import filecmp
from tempfile import NamedTemporaryFile
import os

MARK = '!'

def make_path(p, sep='_'):
    '''Find a similar, yet unused path'''
    p = path(p)
    name, ext = p.splitext()
    n = 1
    while p.exists():
        p = path(name + '%s%s%s' % (sep, n, ext))
        n += 1
    return p

def same_file(p, pp):
    return filecmp.cmp(p, pp)

def mktemp():
    f = NamedTemporaryFile(delete=False)
    f.close()
    loc = path(f.name)
    loc.remove()
    return loc

def noop(*args, **kwargs):
    '''does nothing'''

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

def correct_ext(pth):
    return pth.splitext()[1] in IMAGE_EXTENSIONS

