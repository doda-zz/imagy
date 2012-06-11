import os.path
import pickle
from config import PROCESSED_LOC
from imagy.utils import make_path
from path import path

class PersistentSet(set):
    def __init__(self, file_loc='', *args, **kwargs):
        super(PersistentSet, self).__init__(*args, **kwargs)
        if file_loc:
            self.load(path(file_loc))
        else:
            self.file_loc = make_path(__file__).abspath()

    def sync(self):
        '''Dump the set of values as a list'''
        with open(self.file_loc, 'w') as f:
            pickle.dump(list(self), f)
    
    def fclear(self):
        '''Clear this instance as well as the file'''
        self.clear()
        self.sync()

    def load(self, file_loc):
        '''
        Load from disk and if purported file location doesnt exist, write an empty PersistentSet there
        '''
        self.file_loc = path(file_loc)
        pth = path(file_loc)
        if not pth.exists():
            self.sync()
            return
        self.clear()
        self.update(pickle.load(open(pth)))
