''' HTTP testing file for auth_logout http function '''
import json
import pytest
import urllib.request
import urllib.parse
from urllib.error import HTTPError
import init_data
import requests

BASE_URL = 'http://127.0.0.1:8080'

class Helpers:
    """
    test class conating helper functions
    """
    @staticmethod
    def urlopen_register(email, password, name_first, name_last):
        """
        Testing Wrapper to open /auth/register for a given email,
        Input: email, password, name_first, name_last
        Output: { u_id, token }
        """

        data = json.dumps({
            "email" : email,
            "password" : password,
            "name_first" : name_first,
            "name_last" : name_last,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={'Content-Type': 'application/json'} )
        payload = json.load(urllib.request.urlopen(req))

        return payload

    @staticmethod
    def urlopen_login(email, password):
        """
        Testing Wrapper to open /auth/login for a given email, 
        Input: email, password
        Output: { u_id, token }
        """
        data = json.dumps({
            "email" : email,
            "password" : password,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/auth/login",
            data=data,
            headers={'Content-Type': 'application/json'} )
        payload = json.load(urllib.request.urlopen(req))

        return payload

    @staticmethod
    def urlopen_logout(token):
        """
        Testing Wrapper to open /auth/login for a given email, 
        Input: token
        Output: { is_success }
        """
        data = json.dumps({
            "token" : token
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/auth/logout",
            data=data,
            headers={'Content-Type': 'application/json'} )
        payload = json.load(urllib.request.urlopen(req))

        return payload

    @staticmethod
    def urlopen_user_all(token):

        queryString = urllib.parse.urlencode({
                "token" : token
            })
        response = requests.get(f"{BASE_URL}/users/all?{queryString}")
        payload = response.json()
        return payload


# This file contains test functions that test auth_logout functionality
# auth_logout takes in a token (string) and returns is_success (boolean)

# These tests assume that auth_register works and Helpers.urlopen_login works

# This function tests whether auth_logout function handles valid token case correctly
def test_auth_logout_valid_token():
    requests.post(f"{BASE_URL}/workspace/reset")

    # Register a new user
    user = Helpers.urlopen_register("jasvirboparoy@gmail.com", "helloWorld1234", "Jasvir", "Boparoy")
    user_id = user['u_id']

    login_user = Helpers.urlopen_login("jasvirboparoy@gmail.com", "helloWorld1234")
    login_user_id = login_user['u_id']

    # Ensure this is the same user that registered and has now logged in
    assert user_id == login_user_id

    token = login_user['token']

    # Check that logout invalidated token for active user
    assert (Helpers.urlopen_logout(token))['is_success'] == True

# This function tests whether function returns access error for an invalid token
def test_auth_logout_invalid_token():
    requests.post(f"{BASE_URL}/workspace/reset")
    
    # Create a fake token that is invalid
    token_1 = "1234573331jasvirB"

    # logging out fake token should throw an access error
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_logout(token_1)

    # Token 2 uses 4 spaces only
    token_2 = "    "

    # Using token 2 should throw access error
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_logout(token_2)