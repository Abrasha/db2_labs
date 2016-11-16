from bson.objectid import ObjectId
from redis import StrictRedis
import pickle
import codecs
import json

print('from' + str(ObjectId('580d26621d7d2d4e6a02813f')))

# a = StrictRedis()
# s = a.set('somekey', json.dumps([{'a': 'mama'}, {'b': 'papa'}]))
# print(json.loads(a.get('somekey').decode('utf-8')))
