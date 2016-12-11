from redis import StrictRedis
from bson.json_util import dumps, loads

cache = StrictRedis()


def is_key_present(key):
    return cache.get(key) is not None


def get_from(_id):
    key = 'from:' + _id
    print('Get from  cache:', key)
    return loads(cache.get(key).decode('utf8'))


def set_from(_id, messages):
    key = 'from:' + _id
    print('Put to cache:', key)
    cache.set(key, dumps(messages))


def get_to(_id):
    key = 'to:' + _id
    print('Get from  cache:', key)
    return loads(cache.get(key).decode('utf8'))


def set_like(like, messages):
    key = 'like:' + like
    print('Put to cache:', key)
    cache.set(key, dumps(messages))


def get_like(like):
    key = 'like:' + like
    print('Get from  cache:', key)
    return loads(cache.get(key).decode('utf8'))


def set_to(_id, messages):
    key = 'to:' + _id
    print('Put to cache:', key)
    cache.set(key, dumps(messages))
