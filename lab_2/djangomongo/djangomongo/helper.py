from pymongo import MongoClient
# from random import randint
from faker import Factory

client = MongoClient()
messages = client['labs']['messages']
users = client['labs']['users']

# for u in users.find():
#     print(u)
#
# for m in messages.find():
#     print(m['body'])

f = Factory.create()


def get_all_users():
    return users.find({})


def get_all_messages():
    return messages.find({})


def get_random_user(count=1):
    res = users.aggregate([{'$sample': {'size': count}}])
    return res.next()


def get_random_message(count=1):
    res = messages.aggregate([{'$sample': {'size': count}}])
    return res.next()


print(get_all_messages())

# insert random messages

messages.delete_many({})
for i in range(500):
    sender_id = get_random_user()['_id']

    while True:
        receiver_id = get_random_user()['_id']
        if receiver_id != sender_id: break

    res = messages.insert_one({
        'title': f.text(),
        'body': f.text(),
        'from': sender_id,
        'to': receiver_id
    })
    print(res.inserted_id)


# insert random users

# for i in range(100):
# users.insert_one({
#         'name': f.name(),
#         'age': randint(5, 50)
#     })
