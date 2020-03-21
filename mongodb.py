from pymongo import MongoClient

class da():
    def __init__(self, ip='127.0.0.1', port=27017):
        self.ip = ip
        self.prot = port
        self.client = MongoClient(ip, port)