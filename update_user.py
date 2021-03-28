import pymongo
import hashlib
import argparse


parser = argparse.ArgumentParser()
   
parser.add_argument('--login', required=True)
parser.add_argument('--passw', required=True)
parser.add_argument('--name', required=True)

args = parser.parse_args()

passw = hashlib.md5(args.passw.encode('utf-8')).hexdigest()

print("")
print("Uzivatelske jmeno: {}".format(args.login))
print("Heslo: {}".format(args.passw))
print("Hash hesla: {}".format(passw))
print("Jmeno: {}".format(args.name))

mdb = pymongo.MongoClient("mongodb://localhost:27017/").IRRADROOM
mdb.users.update_one({'user': args.login}, {'$set': {'user': args.login, 'pass': passw, 'name': args.name, 'level': 100}}, upsert=True )