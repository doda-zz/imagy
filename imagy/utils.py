from path import path
import filecmp

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
