# -*- coding: utf-8 -*-

import unittest
from imgtest import ImagyTestCase
from imagy.config import *
from imagy.core import *
from imagy.store import Store

import logging
logging.disable(logging.CRITICAL)

class CoreTestSuite(ImagyTestCase):
    def setup(self):
        self.s = Store()
        self.copy_images_over()

    def check_image(self, img):
        img = self.img_path(img)
        sz = img.size
        compress_with_touch(img)
        self.assertTrue(sz >= img.size)

    def test_store_original(self):
        img = self.img_path('jpg')
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
    # dynamically add tests for various file formats, SO FN DRY
    for typ in ImagyTestCase.image_files:
        fn = lambda self:self.check_image(typ)
        setattr(CoreTestSuite, 'test_%s' % typ, fn)
    unittest.main()

if __name__ == '__main__':
    main()
