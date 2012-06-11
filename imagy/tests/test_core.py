# -*- coding: utf-8 -*-

import unittest
from imagy.config import *
from imagy.core import *
from tempfile import mktemp
from path import path
import logging
logging.disable(logging.CRITICAL)


class TinyTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.image_loc = path('images/')
        self.tmp_image_loc = path('imagesTEMP/')
        images = {
            'png':'png.png',
            'jpg':'jpg.jpg',
            'gif':'gif.gif',
            'gifgif':'gifgif.gif'
            }

        self.images = dict((k, self.image_loc.joinpath(v)) for k, v in images.items())
        self.image_loc.copytree(self.tmp_image_loc)

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

if __name__ == '__main__':
    unittest.main()
