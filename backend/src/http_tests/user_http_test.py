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
    
    
    
def user_profile(token):
    '''
    GET
    '''
    string = 'token=' + token
    req = urllib.request.urlopen(f"{BASE_URL}/user/profile?{string}")
    payload = json.load(req)
    return payload
    
    
    
   
def test_user_profile_is_working():
    '''
    GET
    given(token, u_id), return {emial, name_first, name_last, handle_str} 
    '''
    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    payload = user_profile(user_one['token'])
    
    assert payload == {
        'u_id' : user_one['u_id'],
        'email' : 'aidenshi@unsw.edu.au',
        'name_first' : 'aiden',
        'name_last' : 'shi',
        'handle_str' : 'aidenshi'
    }
    
    
def user_profile_setname(token, name_first, name_last):
    '''
    PUT
    '''
    data = json.dumps({
        'token' : token,
        'name_first' : name_first,
        'name_last' : name_last
    })
    
    headers = {"content-type": "application/json", "Authorization": "<auth-key>" }

    response = requests.put(f"{BASE_URL}/user/profile/setname", data=data, headers=headers)
    


    
def test_user_profile_setname_is_working():
    '''
    PUT
    given(token, name_first, name_last), return {} 
    '''
    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    #reset name
    user_profile_setname(user_one['token'], 'danile', 'lee')
    
    payload = user_profile(user_one['token'])
    
    assert payload == {
        'u_id' : user_one['u_id'],
        'email' : 'aidenshi@unsw.edu.au',
        'name_first' : 'danile',
        'name_last' : 'lee',
        'handle_str' : 'aidenshi'
    }
    

def user_profile_setemail(token, email):
    '''
    PUT
    '''
    data = json.dumps({
        'token' : token,
        'email' : email
    })
    
    headers = {"content-type": "application/json", "Authorization": "<auth-key>" }

    response = requests.put(f"{BASE_URL}/user/profile/setemail", data=data, headers=headers)


    
def test_user_profile_setemail_is_working():
    '''
    PUT
    given(token, email), return {} 
    '''
    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    #reset eamil
    user_profile_setemail(user_one['token'], 'z5255218@unse.edu.au')

    payload = user_profile(user_one['token'])
    
    assert payload == {
        'u_id' : user_one['u_id'],
        'email' : 'z5255218@unse.edu.au',
        'name_first' : 'aiden',
        'name_last' : 'shi',
        'handle_str' : 'aidenshi'
    }
    
    
def user_profile_sethandle(token, handle_str):
    '''
    PUT
    '''
    data = json.dumps({
        'token' : token,
        'handle_str' : handle_str
    })
    
    headers = {"content-type": "application/json", "Authorization": "<auth-key>" }

    response = requests.put(f"{BASE_URL}/user/profile/sethandle", data=data, headers=headers)


    
def test_user_profile_sethandle_is_working():
    '''
    PUT
    given(token, email), return {} 
    '''
    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    #reset handle string
    user_profile_sethandle(user_one['token'], 'i am the best')

    payload = user_profile(user_one['token'])
    
    assert payload == {
        'u_id' : user_one['u_id'],
        'email' : 'aidenshi@unsw.edu.au',
        'name_first' : 'aiden',
        'name_last' : 'shi',
        'handle_str' : 'i am the best'
    }
     
    
def users_all(token):
    '''
    GET
    '''
    string = 'token=' + token
    req = urllib.request.urlopen(f"{BASE_URL}/users/all?{string}")
    payload = json.load(req)
    return payload
    
    
    
    
def test_users_all_is_working():
    '''
    GET
    given(token), return{users}
    Returns a list of all users and their associated details
    '''
    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    payload = users_all(user_one['token'])
    
    assert payload == {
        'users' : [
            {
                "u_id" : user_one['u_id'],
                "email" : "aidenshi@unsw.edu.au",
                "name_first" : "aiden",
                "name_last" : "shi",
                "handle_str" : "aidenshi"
            }
        ]
    }
    
    
    
    
    
    
    


