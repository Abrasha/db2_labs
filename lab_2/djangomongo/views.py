from bson.objectid import ObjectId
from dbus.exceptions import UnknownMethodException
from django.shortcuts import render_to_response, redirect

from lab_2.djangomongo.data import supplier
import re

from lab_2.djangomongo.data.supplier import get_messages_count, get_users_count, get_user_statistics


def index(request):
    return redirect('messages')


def messages(request):
    if request.method == 'GET':
        return get_messages(request)
    elif request.method == 'POST':
        send_message(request)
        return redirect('messages')
    else:
        raise UnknownMethodException('Unsupported method: ' + request.method)


def delete_messages(request):
    if request.method == 'POST':
        params = request.POST
        _id = params['_id']
        print('Attempt to delete: ', _id)
        supplier.remove_message(params['_id'])
        return redirect('messages')
    else:
        raise UnknownMethodException('Unsupported method: ' + request.method)


def get_users(request):
    if request.method == 'GET':
        return render_to_response('users.html', {
            'users_count': get_users_count(),
            'title': 'Users',
            'users': list(get_user_statistics())
        })
    else:
        raise UnknownMethodException('Unsupported method: ' + request.method)


def get_messages(request):
    params = request.GET
    if 'from' in params:  # show messages from him
        title = 'Messages from ' + str(supplier.get_user(params['from'], {'name': 1})['name'])
        messages_result = supplier.get_messages_from(params['from'])
    elif 'to' in params:  # show messages to him
        title = 'Messages to ' + str(supplier.get_user(params['to'], {'name': 1})['name'])
        messages_result = supplier.get_messages_to(params['to'])
    elif 'contains' in params:  # show messages that contain given string
        title = 'Search messages contains ' + params['contains']
        if 'case_insensitive' in params:
            messages_result = supplier.get_messages_body_like(re.compile(params['contains'], re.IGNORECASE))
        else:
            messages_result = supplier.get_messages_body_like(params['contains'])
    else:
        title = 'All messages'
        limit = params['limit'] if 'limit' in params else 100
        messages_result = supplier.get_all_messages_with_people(int(limit))

    messages_result = list(messages_result)
    number_of_messages = len(messages_result)

    return render_to_response('messages.html', {
        'messages_count': get_messages_count(),
        'title': title,
        'messages': messages_result,
        'number_of_messages': number_of_messages,
        'users': list(supplier.get_all_users())
    })


def send_message(request):
    params = request.POST
    message = {
        'from': ObjectId(params['from']),
        'to': ObjectId(params['to']),
        'title': params['title'],
        'body': params['body'],
    }
    supplier.insert_message(message)
