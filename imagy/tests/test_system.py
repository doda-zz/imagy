# -*- coding: utf-8 -*-

import unittest
from imagy.config import *
from imagy.core import *
from imagy.persistence import load as load_pers, processed
print 'test', processed
from tempfile import mktemp
from path import path
from tempfile import mktemp
from subprocess import Popen as p, call as c
import test

import logging
logging.disable(logging.CRITICAL)


class TinyTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.tmp = path(mktemp())
        tmp.mkdir()
        self.proc = p(['imagy', tmp])

    def tearDown(self):
        pass

    def test_create(self):
        img = images['jpg']
        new = make_path(img)
        img.copy(new)
        # fail if no visible optimization has occured after 10 seconds
        for _ in range(10):
            if img.size > new.size:
                break
            time.sleep(1)
        self.assertTrue(img.size > new.size)

    def test_revert(self):
        ret = c(['imagy', '-r'])
        self.assertEqual(ret, 0)
        self.assertFalse(self.tmp.files('*%s*' % ORIGINAL_IDENTIFIER))
        self.assertEqual(len(self.tmp.files()), len(test.images))

if __name__ == '__main__':
    unittest.main()
