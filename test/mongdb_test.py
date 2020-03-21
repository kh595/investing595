import mongodb
import unittest

class Test_mogodbAdaptor(unittest.TestCase):
    def setUp(self):
        self.da = mongodb.da()
        self.db = self.da.client['test']
        self.collection = self.db['test_collection']
        self.collection.insert_one({'id':1, 'value':'값#1'})

    def tearDown(self):
        self.collection.drop()

    def test_insert(self):        
        self.collection.insert_one({'id':2, 'value':'값#2'})

    def test_get_db_collection_name(self):       
        result = self.db.list_collection_names()
        self.assertNotEqual(len(result), 0)

    def test_collection_find_one(self):
        result = self.collection.find_one()
        print(result)
        self.assertNotEqual(len(result), 0)