from __future__ import division
from path import path
from context import imagy
from subprocess import Popen as p, call as c
import unittest
from operator import eq
from tempfile import mkdtemp
import time


root = path(__file__)
image_loc = root.parent.joinpath('images')
image_files = {
    'png':'png.png',
    'jpg':'jpg.jpg',
    'gif':'gif.gif',
    'gifgif':'gifgif.gif'
    }
images = dict((k, image_loc.joinpath(v)) for k, v in image_files.items())

QUIET = True

class ImagyTestCase(unittest.TestCase):
    def wait_until_passes(self, valfun, genfun=eq, classfun='assertEqual', sleep=10, res=0.5):
        '''
        wait upto x seconds for the test to pass
        incredibly hackish and probably not `the` way to do it, but alas..
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
        if not self.tmp:
            self.mktemp()
        self.proc = p(['imagy', '-q' if QUIET else '', self.tmp])

    def copy_images_over(self):
        c(['cp'] + images.values() + [self.tmp])
