from redis import StrictRedis
from bson.json_util import dumps, loads

cache = StrictRedis()


def get_from(_id):
    return loads(cache.get('from:' + _id).decode('utf8'))


def is_key_present(key):
    return cache.get(key) is not None


def set_from(_id, messages):
    cache.set('from:' + _id, dumps(messages))
