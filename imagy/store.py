from path import path
import pickle
import logging
from collections import defaultdict

class Store(object):
    '''
    Keeps track of originals and - optionally - persists them to disk
    the actual dictionaries alongside their respective pickle paths get created dynamically with get/setattr
    '''
    STORES = (
        # used if we mess with a file and don't want watchdog to pick it up
        ('ignored', lambda:defaultdict(int), 'ignored.p'),
        # used to restore original files in case of --revert
        ('originals', dict, 'originals.p'),
        # maintained to quickly check if a stored original has been modified
        # if we mark it and ask what to do upon --revert
        ('storedat', dict, 'storedat.p'),
        )
              
    def __init__(self, dir=None):
        self.locations = {}
        self.clear()
        self.dir = dir
        if dir is None:
            self.clear()
        else:
            self.load(dir)

    def clear(self):
        '''initialize data stores to emptiness'''
        for name, typ, loc in self.STORES:
            setattr(self, name, typ())
            
    def load(self, dir):
        '''tries to load files from the dir, if the directory or a file doesn't exist, do nothing'''
        self.dir = dir = path(dir)
        if not dir.exists():
            return
        for name, typ, loc in self.STORES:
            thing_loc = dir.joinpath(loc)
            self.locations[name] = thing_loc
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
            pickle.dump(getattr(self, name), open(self.locations[name], 'w'))

    def ignore(self, item, n=1):
        '''increment the counter inside ignored, which causes events to that path to be ignored n times'''
        self.ignored[item] += n
        
    def wants(self, pth):
        '''
        Returns if the pth is supposed to be optimized
        to work around watchdog picking up modified file paths at an indeterminate point
        in time, we maintain a counter of how many times to ignore it
        e.g. if we create a new file in a directory that watchdog is watching we can expect to receive
        2 events, file_created and file_modified and increase its counter to 2
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
