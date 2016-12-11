from random import randint

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


# insert random messages
def insert_random_messages(count):
    all_users = list(get_all_users())
    users_count = len(all_users)
    items = []
    for i in range(count):
        sender_id = all_users[randint(0, users_count - 1)]['_id']

        while True:
            receiver_id = get_random_user()['_id']
            if receiver_id != sender_id:
                break

        items.append({
            'title': f.text(),
            'body': f.text(),
            'from': sender_id,
            'to': receiver_id
        })
        print('Generated message # ' + str(i))

    messages.insert_many(items)
    print('Done inserting messages. count = ', count)


# insert random users
def insert_random_users(count):
    items = []
    for i in range(count):
        items.append({
            'name': f.name(),
            'age': randint(5, 50)
        })
        # print('Inserted # ' + i)
        print('Generated user # ' + str(i))

    users.insert_many(items)
    print('Done inserting users. count = ', count)

# insert_random_users(100)

# insert_random_messages(1000)
