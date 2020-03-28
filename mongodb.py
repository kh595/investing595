from pymongo import MongoClient
import pandas as pd

class da():
    def __init__(self, ip='127.0.0.1', port=27017):
        self.ip = ip
        self.prot = port
        self.client = MongoClient(ip, port)

    def insert_new(self, target_collection, new_df, index_str):
        target_df = pd.DataFrame(list(target_collection.find()))
        del target_df['_id']
        target_df = target_df.set_index(index_str).sort_index(ascending=False)

        add_df = new_df[~new_df.index.isin(target_df.index)]

        if add_df.empty == False:
            target_collection.insert_many(new_df[~new_df.index.isin(target_df.index)].reset_index().to_dict('records'))

    def collection_to_df(self, collection, index_str):        
        tlist = list(collection.find())
        if len(tlist) == 0:
            return None
        sdf = pd.DataFrame(tlist)        
        del sdf['_id']
        sdf = sdf.set_index(index_str)
        sdf = sdf.sort_index(ascending=False)
        return sdf