import pytest
import urllib.request
import json
import requests
import urllib

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
    req = urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/auth/register", data=data, headers={'Content-Type': 'application/json'}))
    
    payload = json.load(req)
    return payload
    
    

def search(token, query_str):
    '''
    GET
    given(token, query_str)
    '''
    string = 'token=' + token + '&query_str=' + query_str
    req = urllib.request.urlopen(f"{BASE_URL}/search?{string}")
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



def test_search_is_working():
    '''
    GET
    given(token, query_str), return{ messages}
    
    Given a query string, return a collection of messages in all of the channels that the user has joined that match the query. Results are sorted from most recent message to least recent message
    '''
    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    #create a new channel
    channel_one = channels_create(user_one['token'], 'my channel', False)

    #send first message
    message_one = message_send(user_one['token'], channel_one['channel_id'], 'i am Aiden!')

    #send second message
    message_two = message_send(user_one['token'], channel_one['channel_id'], 'How are u')

    payload = search(user_one['token'], 'am')
    
    assert payload == {
        'messages' : [
            'i am Aiden!',
        ]
    }
    
