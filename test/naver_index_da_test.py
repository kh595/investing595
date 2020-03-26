import naver 
import unittest   # The test framework

class Test_testNaverDataAdapter(unittest.TestCase):
    def setUp(self):
        self.da = naver.index_da()

    def test_get_world_symbol(self):
        self.assertEqual(self.da.get_world_symbol('dow'), 'DJI@DJI')   
    
    def test_get_world_symbol_no_symbol(self):
        self.assertEqual(self.da.get_world_symbol('nosymobl'), None)         

    def test_get_data_kor_index(self):
        self.assertNotEqual(len(self.da.get_ts_data_kor_index('kospi', 3)), 0)
    
    def test_get_data_world_index(self):
        self.assertNotEqual(len(self.da.get_ts_data_world_index('dow', 3)), 0)               

    def test_get_data_exchange(self):
        self.assertNotEqual(len(self.da.get_ts_data_exchange('$',3)), 0)
        
    def test_get_data_oil(self):
        self.assertNotEqual(len(self.da.get_ts_data_oil('oil',3)), 0)

    def test_get_data_interest(self):
        self.assertNotEqual(len(self.da.get_ts_data_interest('interest',3)), 0)

if __name__ == '__main__':
    unittest.main()