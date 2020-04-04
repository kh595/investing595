import sys
import os
sys.path.append(os.path.abspath('./Common'))

import DataAdaptor
import unittest

class Test_da(unittest.TestCase):
    def setUp(self):
        self.da = DataAdaptor.DataAdaptor()

    def tearDown(self):
        pass
    
    def test_da(self):
        self.assertIsNotNone(self.da)