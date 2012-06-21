# -*- coding: utf-8 -*-

import unittest
import time
from imgtest import *
from imagy.config import *
from imagy.core import *
from path import path
from tempfile import mkdtemp
from subprocess import Popen as p, call as c

import logging
logging.disable(logging.CRITICAL)

ORIGINALS = '*%s*' % ORIGINAL_IDENTIFIER


class TinyTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.tmp = ''

    def tearDown(self):
        if self.tmp:
            self.tmp.rmtree()

    def start(self):
        if not self.tmp:
            self.mktemp()
        self.proc = p(['imagy', '-q', self.tmp])

    def mktemp(self):
        self.tmp = path(mkdtemp())

    def test_watch(self):
        self.mktemp()
        self.start()
        time.sleep(1)
        c(['cp'] + images.values() + [self.tmp])
        while 1:
            time.sleep(0.1)
            if 8 == len(self.tmp.files()):
                break
        time.sleep(10)
        self.assertEqual(8, len(self.tmp.files()))
        self.assertEqual(4, len(self.tmp.files(ORIGINALS)))

    def test_revert(self):
        return
        ret = c(['imagy', '-r'])
        self.assertEqual(ret, 0)
        self.assertFalse(self.tmp.files('*%s*' % ORIGINAL_IDENTIFIER))
        self.assertEqual(len(self.tmp.files()), len(test.images))

if __name__ == '__main__':
    unittest.main()



'''
mkdir
start
move all files
check if there are 4 files *ident*
check if they are all smaller than their ident, ''
check if all the originals are the same files

'''
