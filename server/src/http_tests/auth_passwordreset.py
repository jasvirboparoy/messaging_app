import pytest
import urllib.request
import json
import requests
import urllib
import init_data
from tests.auth_passwordreset_request_test import get_reset_code
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

def auth_passwordreset_request(email):
    '''
    POST
    input: email
    return: {}

    Given an email address, if the user is a registered user,
    send's them a an email containing a specific secret code,
    that when entered in auth_passwordreset_reset,
    shows that the user trying to reset the password is the one who got sent this email.
    '''
    data = json.dumps({
        'email' : email,
    }).encode('utf-8')
    
    req = urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/auth/passwordreset/request", data=data, headers={'Content-Type': 'application/json'}))
    
    payload = json.load(req)
    return payload
    

    


def auth_passwordreset_reset(reset_code, new_password):
    '''
    POST
    input: reset_code, new_password
    return: {}
    Given a reset code for a user, set that user's new password to the password provided
    '''
    data = json.dumps({
        'reset_code' : reset_code,
        'new_password' : new_password
    }).encode('utf-8')
    
    req = urllib.request.urlopen(urllib.request.Request(f"{BASE_URL}/auth/passwordreset/reset", data=data, headers={'Content-Type': 'application/json'}))
    
    payload = json.load(req)
    return payload
    
'''
def test_auth_passwordreset_request_and_auth_passwordreset_reset_is_working():

    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aiden1747960409@gmail.com", "123!@#asd", "aiden", "shi")

    #email = given_u_id_find_email(user_one['u_id'])
    email = 'aiden1747960409@gmail.com'
    
    auth_passwordreset_request(email)
    
    reset_code_user_get = get_reset_code
    
    reset_code_in_data_base = init_data.PASSWORD_RESET[0]['reset_code']

    assert reset_code_in_data_base == reset_code_user_get


# given u_id find email
def given_u_id_find_email(u_id):
    
    email = init_data.USER_DICT[u_id]['email']
    
    return email
    

'''

def test_auth_passwordreset_request_and_auth_passwordreset_reset_is_working():

    #reset
    requests.post(f"{BASE_URL}/workspace/reset")

    #register a user
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    #email = given_u_id_find_email(user_one['u_id'])
    email = 'aiden1747960409@gmail.com'
    
    reset_code = '123456'
    init_data.PASSWORD_RESET[0]['reset_code'] = '123456'
    init_data.PASSWORD_RESET[0]['email'] = 'aiden1747960409@gmail.com'
    
    
    auth_passwordreset_reset(reset_code, 'comp1531')
    
    u_id = ''
    
    for key in init_data.USER_DICT:
        u_id = key
    
    
    assert init_data.USER_DICT[u_id]['password'] == 'comp1531'





