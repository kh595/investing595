import unittest  # The test framework
import etc_source

class Test_testNaverDataAdapter(unittest.TestCase):
    def setUp(self):
        self.da = etc_source
    
    def test_get_today_stock_price_by_url(self):
        url = 'http://stock.hankyung.com/apps/rank.panel_sub?market=1'
        self.assertNotEqual(len( self.da.get_today_stock_price_by_url(url)), 0)
    
    def test_get_today_stock_price_kospi(self):
        self.assertNotEqual(len( self.da.get_today_stock_price('kospi')), 0)

    def test_get_today_stock_price_kosdaq(self):
        self.assertNotEqual(len( self.da.get_today_stock_price('kosdaq')), 0)

if __name__ == '__main__':
    unittest.main()
