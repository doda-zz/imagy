# -*- coding: utf-8 -*-

import unittest
from imagy.config import *
from imagy.persistence import PersistentSet
from tempfile import mktemp
from path import path
import pickle
import logging
logging.disable(logging.CRITICAL)

class PersistenceTestSuite(unittest.TestCase):
    """Test cases for persistence."""

    def setUp(self):
        self.s = PersistentSet(mktemp())

    def tearDown(self):
        self.s.file_loc.remove()

    def test_load(self):
        s = set('ads')
        t = mktemp()
        pickle.dump(s, open(t, 'w'))
        self.s.load(t)
        self.assertTrue(s.issubset(self.s))
        
    def test_sync(self):
        thing = 'syncer'
        self.s.add(thing)
        self.s.sync()
        self.s.load(self.s.file_loc)
        self.assertTrue(thing in self.s)

    def test_fclear(self):
        thing = 'asd'
        self.s.add(thing)
        self.s.fclear()
        self.s.load(self.s.file_loc)
        self.assertFalse(thing in self.s)
        
if __name__ == '__main__':
    unittest.main()
