import unittest  # The test framework

import naver


class Test_testNaverDataAdapter(unittest.TestCase):
    def setUp(self):
        self.da = naver.stock_da()

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

    def test_get_main_tosajungbo(self):
        self.assertEqual(self.da.get_main_투자정보('035420')['액면가'], 100)

    def test_get_main_jonghapjungbo_giup_siljuk_bunsuk(self):
        self.assertNotEqual(len(self.da.get_종합정보_기업실적분석('035420')), 0)

    def test_get_main_jonghapjungbo_giup_siljuk_bunsuk_yungan(self):
        self.assertNotEqual(len(self.da.get_종합정보_기업실적분석_연간('035420')), 0)

    def test_get_main_jonghapjungbo_giup_siljuk_bunsuk_bungi(self):
        self.assertNotEqual(len(self.da.get_종합정보_기업실적분석_분기('035420')), 0)

if __name__ == '__main__':
    unittest.main()
