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
        self.copy_images_over(1)
        valfun = lambda:(2, len(self.tmp.files()))
        self.wait_until_passes(valfun, sleep=20)

    def test_init_revert(self):
        self.copy_images_over(1)
        self.start('--no-watch', starter=call)
        valfun = lambda:(2, len(self.tmp.files()))
        self.wait_until_passes(valfun)
        self.start('-r', starter=call)
        valfun = lambda:(1, len(self.tmp.files()))
        self.wait_until_passes(valfun)

    def test_del_originals(self):
        self.copy_images_over(1)
        self.start('--no-watch', starter=call)
        valfun = lambda:(2, len(self.tmp.files()))
        self.wait_until_passes(valfun)
        self.start('--deloriginals', starter=call)
        valfun = lambda:(1, len(self.tmp.files()))
        self.wait_until_passes(valfun)

    def test_files_mode(self):
        self.copy_images_over(1)
        self.start('-m', '-f', *self.tmp.files(), starter=call)
        self.assertEqual(2, len(self.tmp.files()))

if __name__ == '__main__':
    unittest.main()
