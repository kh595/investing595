import naver 
import unittest   # The test framework

class Test_testNaverDataAdapter(unittest.TestCase):
    def setUp(self):
        self.da = naver.da()

    def test_get_world_symbol(self):
        self.assertEqual(self.da.get_world_symbol('dow'), 'DJI@DJI')   
    
    def test_get_world_symbol_no_symbol(self):
        self.assertEqual(self.da.get_world_symbol('nosymobl'), None)         

    def test_get_code_by_name(self):
        self.assertEqual(self.da.get_code_by_name('NAVER'), '035420')

    def test_get_code_by_name_no_name(self):
        self.assertEqual(self.da.get_code_by_name('no_name'), None)

    def test_get_url_by_name_no_name(self):
        self.assertEquals(self.da.get_url_by_name('notin'), None)

    def test_get_url_by_name(self):
        self.assertEqual(self.da.get_url_by_name('NAVER'), 'http://finance.naver.com/item/sise_day.nhn?code=035420')

    def test_get_url_by_code(self):
        self.assertEqual(self.da.get_url_by_code('035420'), 'http://finance.naver.com/item/sise_day.nhn?code=035420')

    def test_get_ts_data(self):
        url = 'http://finance.naver.com/item/sise_day.nhn?code=035420'
        self.assertNotEqual(len(self.da.get_ts_data(url, range_num=2, table_num=0, date_str='날짜')), 0)

    def test_get_data_kor_stock(self):
        self.assertNotEqual(len(self.da.get_ts_data_kor_stock('NAVER', 2)), 0)

    def test_get_data_kor_index(self):
        self.assertNotEqual(len(self.da.get_ts_data_kor_index('kospi', 2)), 0)
    
    def test_get_data_world_index(self):
        self.assertNotEqual(len(self.da.get_ts_data_world_index('dow', 2)), 0)

if __name__ == '__main__':
    unittest.main()