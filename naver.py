import pandas as pd
import numpy as np
from datetime import datetime
import requests
from bs4 import BeautifulSoup

import krx
import mongodb
import DataAdaptor

class naver_da(DataAdaptor.DataAdaptor):
    def __init__(self):
        super().__init__()

    def get_ts_data(self, url, range_num=200, table_num=0, date_str='날짜'):
        print("요청 URL = {}".format(url))
        
        df = pd.DataFrame()
        for page in range(1,range_num):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0, encoding='euc-kr')[table_num], ignore_index=True)

        df = df.dropna()
        df[date_str] = pd.to_datetime(df[date_str])
        df = df.set_index(date_str)
        return df 

class stock_da(naver_da):
    def __init__(self):
        super().__init__()
        self.code_df = krx.get_code_df()
    
    def get_code_by_name(self, item_name):
        retVal = self.code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
        if retVal == 'Series([], )':
            return None
        else:
            return retVal

    def get_url_by_name(self, item_name):
        code = self.get_code_by_name(item_name)
        if code == None:
            return None
        else:
            return self.get_url_by_code(code)

    def get_url_by_code(self, item_code):
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=item_code)
        return url

    def get_ts_data_kor_stock(self, stock_name, range_num=200):
        url = self.get_url_by_name(stock_name)
        return self.get_ts_data(url, range_num)

    # self.assertEqual(self.da.get_main_투자정보('035420')['액면가'], 100)
    def get_main_투자정보(self, code):    
        URL = "https://finance.naver.com/item/main.nhn?code=%s" % (code)
        html = requests.get(URL).text
        soup = BeautifulSoup(html, 'html.parser')
        finance_html = soup.select('table.per_table')

        per = finance_html[0].find(id='_per')
        pbr = finance_html[0].find(id='_pbr')
        시총 = soup.select('div.first')[0].find(id='_market_sum')
        액면가 = soup.select('div.first table')[0].select('tr')[3].select('td em')

        if per is not None:
            per = float(per.text.replace(',',''))
        if pbr is not None:
            pbr = float(pbr.text.replace(',',''))
        if 시총 is not None:
            시총 = int(시총.text.strip().replace('\n','').replace('\t','').replace(',','').replace('조',''))
        if 액면가 is not None:
            액면가 = int(액면가[0].text)
        
        return {'per':per, 'pbr':pbr, '시총':시총, '액면가':액면가}

    def get_종합정보_기업실적분석(self, code):
        URL = "https://finance.naver.com/item/main.nhn?code=%s" % (code)
        html = requests.get(URL).text
        soup = BeautifulSoup(html, 'html.parser')

        div = soup.find('div', {"class":'section cop_analysis'})
        if div is None:
            return None
        table = div.select('table')[0]
        table_rows = table.find_all('tr')

        res = []
        index_name = []
        col_name = [th.text.strip() for th in table_rows[1].find_all('th')]

        for tr in table_rows:            
            td = tr.find_all('td')
            row = [tr.text.strip().replace(',','') for tr in td if tr.text]
            if row:
                index_name.append( tr.find('th').text)
                res.append(row)

        return pd.DataFrame(index=index_name, columns=col_name, data=res)

    def get_종합정보_기업실적분석_연간(self, code):
        tdf = self.get_종합정보_기업실적분석(code)
        if tdf is None:
            return None
        if tdf.empty:
            return None   

        ttdf = tdf.iloc[:,:4]           
        # ttdf.columns = pd.to_datetime(['2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31'])
        return ttdf.transpose()

    def get_종합정보_기업실적분석_분기(self, code):
        tdf = self.get_종합정보_기업실적분석(code)
        if tdf is None:
            return None
        if tdf.empty:
            return None        

        ttdf = tdf.iloc[:,4:]
        # ttdf.columns = pd.to_datetime(['2018-12-31', '2019-03-31', '2019-06-30', '2019-09-30', '2019-12-31', '2020-03-31'])
        return ttdf.transpose()   
    
    def get_펀더멘털(self, code):
        url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}".format(code)
        try:
            dfs = pd.read_html(url)
        except:
            return None
        if (len(dfs) > 5):        
            return pd.read_html(url)[5]
        else:
            return None
   
class index_da(naver_da):
    def __init__(self):
        super().__init__()
        self.symbol_dic = {'dow':'DJI@DJI', 'nasdaq':'NAS@IXIC', 'sp':'SPI@SPX', 'sh':'SHS@000001'}
        self.exchang_dic = {'$':'FX_USDKRW'}

    def get_world_symbol(self, name):
        if name in self.symbol_dic.keys():
            return self.symbol_dic[name]
        else:
            return None

    def get_ts_data_kor_index(self, index_name, range_num=200):
        url = "https://finance.naver.com/sise/sise_index_day.nhn?code={taget_name}".format(taget_name=index_name)
        return self.get_ts_data(url, range_num)   

    def get_ts_data_exchange(self, name, range_num=200):
        currency_name = self.exchang_dic[name]
        url = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd={taget_name}".format(taget_name=currency_name)
        return self.get_ts_data(url, range_num)                            

    def get_ts_data_oil(self, name, range_num=200):
        url = "https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=OIL_CL&fdtc=2"
        return self.get_ts_data(url, range_num)         

    def get_ts_data_interest(self, name, range_num=200):
        url = "https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_CD91"
        return self.get_ts_data(url, range_num)         
    
    def get_ts_data_world_index(self, name, range_num=200):        
        symbol = self.get_world_symbol(name)
        date_str = 'xymd'
        
        url = "https://finance.naver.com//world/worldDayListJson.nhn?symbol={symbol}&fdtc=0".format(symbol=symbol)
        print("요청 URL = {}".format(url))
        
        df = pd.DataFrame()
        
        for page in range(1,range_num):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_json(pg_url))

        df = df.dropna()
        df[date_str] = pd.to_datetime(df[date_str], format='%Y%m%d')
        df = df.set_index(date_str)

        return df 
