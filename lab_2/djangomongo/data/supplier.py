from bson import Code
from bson import ObjectId
from pymongo import MongoClient
from lab_2.djangomongo.data import cache

client = MongoClient()
messages = client['labs']['messages']
users = client['labs']['users']


def get_messages_count():
    return messages.count()


def get_users_count():
    return users.count()


def get_all_users():
    return users.find({})


def get_user_statistics():
    mapper = Code("""
        function(){
            emit(this.from, this.body.split(' ').length);
        }
    """)

    reducer = Code("""
        function(from, words_count){
            return Array.sum(words_count) / words_count.length;
        }
    """)

    result = messages.map_reduce(mapper, reducer, out='words_average')

    for entry in result.find({}):
        user = get_user(entry['_id'])
        yield ({
            '_id': user['_id'],
            'name': user['name'],
            'age': user['age'],
            'average': entry['value']
        })


def get_all_messages(limit=0):
    return messages.find({}).limit(limit)


def get_all_messages_with_people(limit=0):
    return get_messages_with_people({}, limit)


def get_messages_with_people(criteria, limit=0, fields=None):
    coll = messages.find(criteria).limit(limit) if fields is None else messages.find(criteria, fields).limit(limit)
    for m in coll:
        yield {
            '_id': m['_id'],
            'from': get_user(m['from']),
            'to': get_user(m['to']),
            'title': m['title'],
            'body': m['body']
        }


def get_messages_body_like(like):
    key = 'like:' + like
    if cache.is_key_present(key):
        return cache.get_like(like)
    else:
        result = list(get_messages_with_people({'body': {'$regex': like}}))
        cache.set_like(key, result)
        return result


def get_messages_from(_id):
    if cache.is_key_present('from:' + _id):
        return cache.get_from(_id)
    else:
        result = list(get_messages_from_raw(_id))
        cache.set_from(_id, result)
        return result


def get_messages_from_raw(_id):
    return get_messages_with_people({'from': ObjectId(_id)})


def refresh_from_cache(_id):
    cache.set_from(str(_id), list(get_messages_from_raw(_id)))


def get_messages_to(_id):
    return get_messages_with_people({'to': ObjectId(_id)})


def get_user(_id, fields=None):
    return users.find_one({'_id': ObjectId(_id)}, fields) if fields is None else users.find_one({'_id': ObjectId(_id)})


def get_message(_id, fields=None):
    return messages.find_one({'_id': ObjectId(_id)}, fields) if fields is None else messages.find_one(
        {'_id': ObjectId(_id)})


def get_random_user(count=1):
    res = users.aggregate([{'$sample': {'size': count}}])
    return res.next()


def get_random_message(count=1):
    res = messages.aggregate([{'$sample': {'size': count}}])
    return res.next()


def insert_message(message):
    messages.insert_one(message)
    if cache.is_key_present('from:' + str(message['from'])):
        refresh_from_cache(message['from'])
    if cache.is_key_present('to:' + str(message['to'])):
        refresh_from_cache(message['to'])


def remove_message(_id):
    message = messages.find({'_id': ObjectId(_id)}).next()
    message_from = message['from']
    message_to = message['to']
    messages.remove({'_id': ObjectId(_id)})
    if cache.is_key_present('from:' + str(message_from)):
        refresh_from_cache(message_from)
    if cache.is_key_present('to:' + str(message_to)):
        refresh_from_cache(message_to)
