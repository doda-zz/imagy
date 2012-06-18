# -*- coding: utf-8 -*-

import unittest
from imagy.config import *
from imagy.core import *
from imagy.utils import mktemp
from imagy.store import Store
from path import path
import imgtest

import logging
logging.disable(logging.CRITICAL)

class TinyTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.images = imgtest.images
        self.loc = imgtest.image_loc
        self.tmp = self.loc.parent.joinpath('imagesTEMP')
        self.loc.copytree(self.tmp)
        self.s = Store()
        self.img_locs = dict((k, self.get_imgp(v)) for k, v in self.images.items())

    def get_imgp(self, img):
        return self.tmp.joinpath(img)

    def tearDown(self):
        self.tmp.rmtree()

    def check_image(self, img):
        img = self.get_imgp(img)
        sz = img.size
        compress_image(img)
        self.assertTrue(sz >= img.size)

    def test_store_original(self):
        img = self.img_locs['jpg']
        orig = store_original(img)
        self.assertTrue(same_file(img, orig))
        orig.remove()
        
    def test_make_path(self):
        self.assertFalse(make_path(__file__).exists())

    def test_clear(self):
        thing = 'thing'
        self.s.originals[thing] = ''
        self.s.clear()
        self.s.save()
        self.assertFalse(thing in self.s.originals)

def main():
    # dynamically tests for various file formats, SO FN DRY
    for typ, pth in imgtest.images.items():
        fn = lambda self:self.check_image(pth)
        setattr(TinyTestSuite, 'test_%s' % typ, fn)
    unittest.main()

if __name__ == '__main__':
    main()
