from path import path
import pickle
import logging
from collections import defaultdict

class Store(object):
    # dynamically created attributes, with their respective pickle paths
    STORES = (
        # used if we mess with a file and don't want watchdog to pick it up
        ('ignored', lambda:defaultdict(int), 'ignored.p'),
        # used to restore original files in case of --revert
        ('originals', dict, 'originals.p'),
        # these are the stored originals, if one of these get modified, 
        # it gets marked so we can later ask what to do upon revert
        ('storedat', dict, 'storedat.p'),
        )
              
    def __init__(self, dir=None):
        self.locs = {}
        self.clear()
        self.dir = dir
        if dir is None:
            self.clear()
        else:
            self.load(dir)

    def clear(self):
        for name, typ, loc in self.STORES:
            setattr(self, name, typ())
            
    def load(self, dir):
        '''tries to load files from the dir, if the directory or a file doesn't exist, do nothing'''
        self.dir = dir = path(dir)
        if not dir.exists():
            return
        for name, typ, loc in self.STORES:
            thing_loc = dir.joinpath(loc)
            self.locs[name] = thing_loc
            if thing_loc.exists():
                setattr(self, name, pickle.load(open(thing_loc)))
                logging.debug('loaded %s from %s', name, thing_loc)

    def save(self):
        '''save to disk, creates directory if necessary'''
        dir = self.dir
        if not dir:
            return
        if not dir.exists():
            dir.mkdir()
        for name, typ, loc in self.STORES:
            pickle.dump(getattr(self, name), open(self.locs[name], 'w'))

    def ignore(self, item, n=1):
        '''increment the counter inside ignored and subsequently ignore it n more times'''
        self.ignored[item] += n
        
    def wants(self, pth):
        '''
        Returns if the pth is supposed to be optimized
        to work around watchdog picking up modified file paths at an indeterminate point
        in time, we maintain a counter of how many times to ignore it (i.e. once if we touch
        a file ourselves)
        '''
        counter = self.ignored[pth]
        if counter < 0:
            # ignore forever
            return False
        elif counter == 0: # default case
            return True
        elif counter > 0:
            self.ignored[pth] -= 1
            return False
            
store = Store()
