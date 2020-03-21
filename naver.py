import pandas as pd
import numpy as np
import krx
import mongodb

from datetime import datetime

class da:
    def __init__(self):
        self.code_df = krx.get_code_df()
        self.symbol_dic = {'dow':'DJI@DJI', 'nasdaq':'NAS@IXIC', 'sp':'SPI@SPX', 'sh':'SHS@000001'}
        self.mongo = mongodb.da()
    
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

    def get_world_symbol(self, name):
        if name in self.symbol_dic.keys():
            return self.symbol_dic[name]
        else:
            return None

    def get_ts_data_kor_index(self, index_name, range_num=200):
        url = "https://finance.naver.com/sise/sise_index_day.nhn?code={index_name}".format(index_name=index_name)
        return self.get_ts_data(url, range_num)                            

    def get_ts_data_kor_stock(self, stock_name, range_num=200):
        url = self.get_url_by_name(stock_name)
        return self.get_ts_data(url, range_num)
    
    def get_ts_data_world_index(self, name, range_num=200):
        symbol = self.get_world_symbol(name)
        url = "https://finance.naver.com/world/sise.nhn?symbol={symbol}".format(symbol=symbol)

        return self.get_ts_data(url, range_num=range_num, table_num=1, date_str="일자")