# -*- coding: utf-8 -*-

import unittest
# todo: remove *s
from imgtest import *
from imagy.config import *
from imagy.core import *
from path import path
from subprocess import Popen as p, call as c

import logging
logging.disable(logging.CRITICAL)

ORIGINALS = '*%s*' % ORIGINAL_IDENTIFIER

class SystemTestSuite(ImagyTestCase):
    """Test system's behavior from afar"""

    def test_watch(self):
        self.create_img_dir()
        self.start()
        # give time for imagy to start
        time.sleep(2)
        self.copy_images_over()
        
        valfun = lambda:(8, len(self.tmp.files()))
        self.wait_until_passes(valfun, sleep=20)

    def test_revert(self):
        return
        ret = c(['imagy', '-r'])
        self.assertEqual(ret, 0)
        self.assertFalse(self.tmp.files('*%s*' % ORIGINAL_IDENTIFIER))
        self.assertEqual(len(self.tmp.files()), len(test.images))

if __name__ == '__main__':
    unittest.main()
