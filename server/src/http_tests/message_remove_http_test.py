import pytest
import urllib.request
import json
import requests
import urllib
import init_data

BASE_URL = 'http://127.0.0.1:8080'


def auth_register(email, password, name_first, name_last):
    '''
    POST
    '''
    data = json.dumps({
        'email' : email,
        'password': password,
        'name_first' : name_first,
        'name_last' : name_last
    }).encode('utf-8')

    headers = {'Content-Type': 'application/json'}

    req = urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/auth/register", data=data, headers=headers))

    payload = json.load(req)
    return payload


def channels_create(token, name, is_public):
    '''
    POST
    given(token, name, is_public)
    return{channel_id}
    '''
    data = json.dumps({
        'token' : token,
        'name': name,
        'is_public' : is_public,
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/channels/create", data=data, headers={'Content-Type': 'application/json'}))

    payload = json.load(req)
    return payload


def message_send(token, channel_id, message):
    ''' 
    POST
    given(token, channel_id, message)
    return{message_id}
    '''
    data = json.dumps({
        'token' : token,
        'channel_id': channel_id,
        'message' : message,
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/message/send", data=data, headers={'Content-Type': 'application/json'}))

    payload = json.load(req)
    return payload


def message_remove(token, message_id):
    '''
    DELETE
    '''
    data = json.dumps({
        'token' : token,
        'message_id' : message_id,
    }).encode('utf-8')
    headers = {'content-type': 'application/json'}
    requests.delete(f"{BASE_URL}/message/remove", data=data, headers=headers)
    return {}


def test_message_remove_is_working():
    '''
    DELETE
    given(token, message_id)
    return{}
    Given a message_id for a message, this message is removed from the channel
    '''

    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    #create a new channel
    channel_one = channels_create(user_one['token'], 'my channel', False)

    #send first message
    message_one = message_send(user_one['token'], channel_one['channel_id'], 'i am Aiden!')


    message_remove(user_one['token'], message_one['message_id'])

    assert init_data.MESSAGES_DICT[channel_one["channel_id"]] == []
