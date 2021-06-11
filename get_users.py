import pymongo
import hashlib
import argparse

mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
print(list(mdb.users.find()))