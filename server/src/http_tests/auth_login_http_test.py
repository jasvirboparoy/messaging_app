''' HTTP testing file for auth http function '''
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

# Function tests cases of invalid email entered for log in
def test_auth_login_invalid_email():
    
    requests.post(f"{BASE_URL}/workspace/reset")

    # Register a user
    Helpers.urlopen_register("jasvirboparoy@gmail.com", "helloWorld", "Jasvir", "Boparoy")

    # personal_info provided, but no domain or @ symbol
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("hello", "123456Hello")

    # domain provided but no personal_info
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("@gmail.com", "1222455Hello")

    # personal_info provided as number but no domain or @ symbol
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("1", "1234567Jb")

    # @ symbol seperator provided but no personal_info or domain
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("@", "1234567Jb")
    
    # @ symbol provided and personal_info provided but no domain
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("///32@", "1234567Jb")

    # Leading space
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login(" jasvirboparoy@gmail.com", "helloWorld")

    # Trailing space
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("jasvirboparoy@gmail.com ", "helloWorld")


# Function tests cases where email provided doesn't belong to a user
def test_auth_login_unregistered_email():
    requests.post(f"{BASE_URL}/workspace/reset")
    # Using valid email to login but hasn't been registered
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("jasvir@gmail.com", "helloWorld")

    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("hello@email.com", "helloWorld")

# Function tests cases where email has been registered and entered email
# matches for log in. It should not throw an exception
def test_auth_login_registered_email():
    requests.post(f"{BASE_URL}/workspace/reset")

    user = Helpers.urlopen_register("jasvirboparoy@gmail.com", "helloWorld", "Jasvir", "Boparoy")
    u_id = user['u_id']
    token = user['token']
   
    # Using all caps for a valid email that has been registered in lowercase
    result_1 = Helpers.urlopen_login("JASVIRBOPAROY@GMAIL.COM", "helloWorld")

    assert result_1['u_id'] == u_id
    # assert result_1['token'] == token (invalid to check this)

    # Using first letter capitalised for valid email that's registered
    result_2 = Helpers.urlopen_login("Jasvirboparoy@gmail.com", "helloWorld")

    assert result_2['u_id'] == u_id
    # Invalid to test this as new token for each session
    # assert result_2['token'] == token


# Function tests cases where incorrect password has been typed
def test_auth_login_incorrect_password():
    requests.post(f"{BASE_URL}/workspace/reset")

    user = Helpers.urlopen_register("jasvirboparoy@gmail.com", "HELLOWORLD1124", "Jasvir", "Boparoy")

    # registered with all caps, entered all lowercase
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("jasvirboparoy@gmail.com", "helloworld1124")

    # Completely wrong password entered
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("jasvirboparoy@gmail.com", "123456Hello")
    
    # Entered one character with wrong case
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("jasvirboparoy@gmail.com", "hELLOWORLD1124")

    # Entered leading space for valid password
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("jasvirboparoy@gmail.com", " HELLOWORLD1124")

    # Entered trailing space for valid password
    with pytest.raises(HTTPError) as e:
        Helpers.urlopen_login("jasvirboparoy@gmail.com", "HELLOWORLD1124 ")

# Function tests cases where correct password has been entered
def test_auth_login_correct_password():
    requests.post(f"{BASE_URL}/workspace/reset")
    
    user = Helpers.urlopen_register("jasvirboparoy@gmail.com", "HELLOWORLD1124", "Jasvir", "Boparoy")
    u_id = user['u_id']
    token = user['token']

    user_login = Helpers.urlopen_login("jasvirboparoy@gmail.com", "HELLOWORLD1124")
    user_login_u_id = user_login['u_id']
    user_login_token = user_login['token']

    assert u_id == user_login_u_id
    # Invalid to test this as new token for new session
    # assert token == user_login_token
