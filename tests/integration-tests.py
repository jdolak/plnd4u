#!/usr/bin/env python3

import unittest
import sys

sys.path.append('./src')
from func_adv import *

class basic_func_tests(unittest.TestCase):
    def test_class_search(self):
        results = db_search_past_classes('Database Concepts',(1,1,1,1,1,1,1,1,1))

        self.assertEqual(len(results), 1, "Too many results")
        self.assertEqual(results, [('CSE 30246', 'Database Concepts')], "Results do not match")
        
if __name__ == '__main__':
    unittest.main()