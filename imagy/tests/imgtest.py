from __future__ import division
from path import path
from context import imagy
from subprocess import Popen, call
import unittest
from operator import eq
from tempfile import mkdtemp
import time

QUIET = 1

class ImagyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ImagyTestCase, self).__init__(*args, **kwargs)
        self.root = path(__file__)
        self.image_loc = self.root.parent.joinpath('images')
        self.image_files = {
            'png':'png.png',
            'jpg':'jpg.jpg',
            'gif':'gif.gif',
            'gifgif':'gifgif.gif'
            }
        self.images = dict((k, self.image_loc.joinpath(v)) for k, v in self.image_files.items())

    def setup(self):
        self.images = images
        self.loc = image_loc
        self.tmp = self.create_img_dir()
        self.s = Store()
        self.img_locs = dict((k, self.get_imgp(v)) for k, v in self.images.items())

    def get_imgp(self, img):
        return self.tmp.joinpath(img)

    def setUp(self, *args, **kwargs):
        self.__setup(*args, **kwargs)
        if not self.__setup is self.setup:
            self.setup(*args, **kwargs)
    
    def tearDown(self, *args, **kwargs):
        self.__teardown(*args, **kwargs)
        if not self.__teardown is self.teardown:
            self.teardown(*args, **kwargs)
    
    def setup(self):
        self.tmp = path(' ')
        self.proc = None
        
    __setup = setup
        
    def teardown(self):
        if self.tmp.exists():
            self.tmp.rmtree()
        if self.proc:
            self.proc.terminate()
            
    __teardown = teardown
        
    def wait_until_passes(self, valfun, genfun=eq, classfun='assertEqual', sleep=10, res=0.5):
        '''
        wait upto `sleep` seconds for the test to pass
        incredibly hackish and very probably not >the< way to do it, but alas..
        '''
        classfun = getattr(self, classfun)
        for _ in range(int(sleep/res)):
            if genfun(*valfun()):
                break
            time.sleep(res)
        classfun(*valfun())

    def create_img_dir(self):
        self.tmp = path(mkdtemp())
    
    def start(self):
        self.proc = Popen(['imagy', '-q' if QUIET else '', self.tmp])

    def copy_images_over(self):
        call(['cp'] + self.images.values() + [self.tmp])
