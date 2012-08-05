from path import path
import logging
from collections import defaultdict, namedtuple
try:
    import simplejson as json
except ImportError:
    import json

SubStore = namedtuple('name init filename mapping')

class Store(object):
    '''
    Keeps track of originals and - optionally - persists them to disk
    the actual dictionaries alongside their respective paths get created dynamically with get/setattr
    the 4th value specifies the individual mappings to allow restoring from JSON
    '''
    STORES = (
        # used if we modify a file and don't want watchdog to pick it up
        SubStore('ignored', lambda *args:defaultdict(int, *args), 'ignored.json', (path, None)),

        # used to restore original files in case of --revert
        SubStore('originals', dict, 'originals.json', (path, path)),

        # maintained to quickly check if a stored original has been modified
        # if we mark it and ask what to do upon --revert
        SubStore('storedat', dict, 'storedat.json', (path, str)),
        )
              
    def __init__(self, dir=None):
        self.filepaths = {}
        self.clear()
        self.dir = dir
        if dir is not None:
            self.load(dir)

    def clear(self):
        '''initialize data stores to emptiness'''
        for substore in self.STORES:
            setattr(self, substore.name, substore.data_type())
            
    def load(self):
        '''tries to load files from the dir, if the directory or a file doesn't exist, do nothing'''
        dir = self.dir = dir = path(dir)
        if not dir.exists():
            return
        for name, data_type, loc, (k_type, v_type) in self.STORES:
        for substore in self.STORES:
            filepath = dir.joinpath(substore.filename)
            self.filepaths[substore.name] = filepath
            try:
                with open(filepath) as f:
                    loaded = json.load(f)
                k_type, v_type = substore.mapping
                value = substore.init((k_type(k), v_type(v)) for k, v in loaded.iteritems())
                setattr(self, substore.name, value)
            except:
                msg = 'couldnt load %s from %s'
                if not filepath.exists():
                    msg += ', no such file'
                logging.debug(msg, name, thing_loc, exc_info=True)
            else:
                logging.debug('successfully loaded %s from %s', name, thing_loc)

    def save(self):
        '''save to disk, creates directory if necessary'''
        dir = self.dir
        if dir is None:
            return
        if not dir.exists():
            dir.makedirs_p()
        for substore in self.STORES:
            with open(self.filepaths[substore.name], 'w') as f:
                json.dump(getattr(self, substore.name), f)

    def ignore(self, item, n=1):
        '''increment the counter inside ignored, which causes events to that path to be ignored n times'''
        self.ignored[item] += n
        
    def wants(self, pth):
        '''
        Returns if the pth is supposed to be optimized
        to work around watchdog picking up modified file paths at an indeterminate point
        in time, we maintain a counter of how many times to ignore it
        e.g. if we create a new file in a directory that watchdog is watching we can expect
        to receive 2 events, file_created and file_modified and increase its counter to 2
        '''
        counter = self.ignored[pth]
        if counter < 0:
            # ignore indefinitely
            return False
        elif counter > 0:
            self.ignored[pth] -= 1
            return False
        # 0 default case
        return True
            
store = Store()

