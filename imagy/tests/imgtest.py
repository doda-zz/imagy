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
    image_files = {
        'png':'png.png',
        'jpg':'jpg.jpg',
        'gif':'gif.gif',
        'gifgif':'gifgif.gif'
        }
    imagy = ['imagy']
    imagy_mem = ['imagy', '-m']
    if QUIET:
        imagy += ['-q']
        imagy_mem += ['-q']
        
    def __init__(self, *args, **kwargs):
        super(ImagyTestCase, self).__init__(*args, **kwargs)
        self.root = path(__file__)
        self.image_loc = self.root.parent.joinpath('images')
        self.images = dict((k, self.image_loc.joinpath(v)) for k,v in self.image_files.items())
        
    def setUp(self, *args, **kwargs):
        self.__setup(*args, **kwargs)
        if not self.__setup is self.setup:
            self.setup(*args, **kwargs)
    
    def tearDown(self, *args, **kwargs):
        self.__teardown(*args, **kwargs)
        if not self.__teardown is self.teardown:
            self.teardown(*args, **kwargs)
    
    def setup(self):
        self.tmp = path(mkdtemp())
        self.proc = None
    __setup = setup
        
    def teardown(self):
        if self.tmp.exists():
            self.tmp.rmtree()
        if isinstance(self.proc, Popen):
            self.proc.terminate()
    __teardown = teardown

    def img_path(self, img):
        return self.tmp.joinpath(self.image_files[img])

    def wait_until_passes(self, valfun, genfun=eq, classfun='assertEqual', sleep=7, res=0.5):
        '''
        doing system testing with unittest ... why not?!
        wait upto `sleep` seconds for the test to pass,
        checking with a generalt function until doing a final test
        with the one associated with the respective TestCase
        '''
        classfun = getattr(self, classfun)
        for _ in range(int(sleep/res)):
            if genfun(*valfun()):
                break
            time.sleep(res)
        classfun(*valfun())

    def start(self, *args, **kwargs):
        starter = kwargs.setdefault('starter', Popen)
        args = self.imagy + list(args)
        self.proc = starter(args + [self.tmp])

    def copy_images_over(self):
        call(['cp'] + self.images.values() + [self.tmp])
