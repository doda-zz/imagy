# -*- coding: utf-8 -*-

import unittest
from imgtest import *
from imagy.config import *
from imagy.core import *
# todo: be less like http://farm3.static.flickr.com/2465/3898431077_b9c5583b12.jpg

import logging
logging.disable(logging.CRITICAL)

ORIGINALS = '*%s*' % ORIGINAL_IDENTIFIER

class SystemTestSuite(ImagyTestCase):
    """Test system's behavior from afar"""

    def test_watch(self):
        self.start('-m')
        # give time for imagy to start
        time.sleep(2)
        self.copy_images_over()

        valfun = lambda:(8, len(self.tmp.files()))
        self.wait_until_passes(valfun, sleep=20)

    def init(self):
        # give time for imagy to start
        self.copy_images_over()
        self.start('-i', starter=call)

    def test_init_revert(self):
        self.init()
        valfun = lambda:(8, len(self.tmp.files()))
        self.wait_until_passes(valfun)
        self.start('-r', starter=call)
        valfun = lambda:(4, len(self.tmp.files()))
        self.wait_until_passes(valfun)

    def test_del_originals(self):
        self.init()
        valfun = lambda:(8, len(self.tmp.files()))
        self.wait_until_passes(valfun)
        self.start('--deloriginals', starter=call)
        valfun = lambda:(4, len(self.tmp.files()))
        self.wait_until_passes(valfun)

    def test_files_mode(self):
        self.copy_images_over()
        call(self.imagy_mem + ['-f'] + self.tmp.files())
        self.assertEqual(8, len(self.tmp.files()))

if __name__ == '__main__':
    unittest.main()
