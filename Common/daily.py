import mongodb
import naver


def insert_new_data():    
    naver_index = naver.index_da() 
    mongo = mongodb.da()
    
    mongo.insert_new(mongo.client.asset.kospi, naver_index.get_ts_data_kor_index('kospi', 2), '날짜')
    mongo.insert_new(mongo.client.asset.kosdaq, naver_index.get_ts_data_kor_index('kosdaq', 2), '날짜')
    
    mongo.insert_new(mongo.client.asset.dow, naver_index.get_ts_data_world_index('dow', 2), 'xymd')
    
    mongo.insert_new(mongo.client.asset.dollar, naver_index.get_ts_data_exchange('$', 2), '날짜')
    
    mongo.insert_new(mongo.client.asset.oil, naver_index.get_ts_data_oil('oil', 2), '날짜')
    
    mongo.insert_new(mongo.client.asset.interest, naver_index.get_ts_data_interest('interest', 2), '날짜')    

    return True
