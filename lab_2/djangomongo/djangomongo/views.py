from bson.objectid import ObjectId
from dbus.exceptions import UnknownMethodException
from django.shortcuts import render_to_response, redirect

from djangomongo.data import supplier
import re


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
        print('Attemp')
        supplier.remove_message(params['_id'])
        pass
    return redirect('messages')


def users(request):
    if request.method == 'GET':
        return render_to_response('users.html', {
            'title': 'Users',
            'users': supplier.get_all_users()
        })
    else:
        raise UnknownMethodException('Unsupported method: ' + request.method)


def get_messages(request):
    params = request.GET
    if 'from' in params:  # show messages from him
        title = 'Messages from ' + str(supplier.get_user(params['from'], {'name': 1})['name'])
        messages_result = supplier.get_messages_from(params['from'])
        pass
    elif 'to' in params:  # show messages to him
        title = 'Messages to ' + str(supplier.get_user(params['to'], {'name': 1})['name'])
        messages_result = supplier.get_messages_to(params['to'])
        pass
    elif 'contains' in params:  # show messages that contain given string
        title = 'Search messages contains ' + params['contains']
        if 'case_insensitive' in params:
            messages_result = supplier.get_messages_body_like(re.compile(params['contains'], re.IGNORECASE))
        else:
            messages_result = supplier.get_messages_body_like(params['contains'])
        pass
    else:
        title = 'All messages'
        messages_result = supplier.get_all_messages_with_people()

    messages_result = list(messages_result)
    number_of_messages = len(messages_result)

    return render_to_response('messages.html', {
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
