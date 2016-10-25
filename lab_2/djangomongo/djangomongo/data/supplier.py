from bson import ObjectId
from pymongo import MongoClient

client = MongoClient()
messages = client['labs']['messages']
users = client['labs']['users']


def get_all_users():
    return users.find({})


def get_all_messages():
    return messages.find({})


def get_all_messages_with_people():
    return get_messages_with_people({})


def get_messages_with_people(criteria, fields=None):
    coll = messages.find(criteria) if fields is None else messages.find(criteria, fields)
    for m in coll:
        yield {
            'from': get_user(m['from']),
            'to': get_user(m['to']),
            'title': m['title'],
            'body': m['body']
        }


def get_messages_body_like(like):
    return get_messages_with_people({'body': {'$regex': like}})


def get_messages_from(_id):
    return get_messages_with_people({'from': ObjectId(_id)})


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
    # TODO return insert result
    messages.insert_one(message)


def remove_message(_id):
    messages.remove({'_id': ObjectId(_id)})
