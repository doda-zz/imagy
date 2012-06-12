# -*- coding: utf-8 -*-

import unittest
from imagy.config import *
from imagy.core import *
from imagy.persistence import load as load_pers, processed
print 'test', processed
from tempfile import mktemp
from path import path
from tempfile import mktemp

import logging
logging.disable(logging.CRITICAL)


class TinyTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.tmp_image_loc = path('imagesTEMP/')
        self.images = test.images
        test.image_loc.copytree(self.tmp_image_loc)
        self.d = processed

    def tearDown(self):
        self.tmp_image_loc.rmtree()

    def test_jpg(self):
        image = self.images['jpg']
        sz = image.size
        compress_image(image, False)
        self.assertTrue(sz >= image.size)

    def test_png(self):
        image = self.images['png']
        sz = image.size
        compress_image(image, False)
        self.assertTrue(sz >= image.size)
        
    def test_gif(self):
        image = self.images['gif']
        sz = image.size
        compress_image(image, False)
        self.assertTrue(sz >= image.size)
        
    def test_gifgif(self):
        image = self.images['gifgif']
        sz = image.size
        opti = compress_image(image, False)
        self.assertTrue(sz >= image.size)

    def test_store_original(self):
        img = self.images['jpg']
        orig = store_original(img)
        self.assertTrue(same_file(img, orig))
        orig.remove()
        
    def test_saught(self):
        self.assertFalse(is_saught_after('/bla/MEOW/asd%s' % PNGNQ_EXT))
        self.assertFalse(is_saught_after('/'))
        
        self.assertTrue(is_saught_after('/png.png'))

    def test_make_path(self):
        self.assertFalse(make_path(__file__).exists())

    def test_clear(self):
        thing = 'asd'
        self.d['set'].add(thing)
        self.d.clear()
        self.d.sync()
        load_pers(self.file_loc)
        self.assertFalse(thing in self.d['set'])

if __name__ == '__main__':
    unittest.main()
