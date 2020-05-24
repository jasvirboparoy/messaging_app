import pytest
import init_data
from urllib.error import HTTPError
from src.error import InputError
from src.workspace import reset_workspace
import urllib
import json
import requests
# This file tests the Helper.auth_register function 
BASE_URL = 'http://127.0.0.1:5390'
# Helper.auth_register takes in email, password, name_first and name_last 
# It returns a u_id and a token

class Helper:
    """
    test class conating helper functions
    """
    @staticmethod
    def auth_register(email, password, name_first, name_last):
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



# Email entered is invalid
def test_auth_register_invalid_email():
    requests.post(f"{BASE_URL}/workspace/reset"
    
    # personal_info provided, but no domain or @ symbol
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("hello", "123456Jasvir", "Jasvir", "Boparoy")

    # domain provided but no personal_info
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")

    # personal_info provided as number but no domain or @ symbol
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("1", "123456Jasvir", "Jasvir", "Boparoy")

    # @ symbol seperator provided but no personal_info or domain
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("@", "123456Jasvir", "Jasvir", "Boparoy")
    
    # @ symbol provided and personal_info provided but no domain
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("///32@", "123456Jasvir", "Jasvir", "Boparoy")

    # Leading space
    with pytest.raises(HTTPError) as e:
        Helper.auth_register(" johnsmith@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")

    # Trailing space
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com ", "123456Jasvir", "Jasvir", "Boparoy")
    reset_workspace()

# Email address is already being used by another user
def test_auth_register_taken_email():
    requests.post(f"{BASE_URL}/workspace/reset")

    Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")

    # Testing using taken email but different password and name
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "111111145Jasvir", "John", "Smith")

    # Testing using taken email with exactly same name and password
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")


# Password entered is less than 6 characters long
# Passwords of less than 6 characters are invalid
def test_auth_register_invalid_password():
    requests.post(f"{BASE_URL}/workspace/reset"

    # Testing numerical password < 6 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "12345", "Jasvir", "Boparoy")

    # Testing lettered password < 6 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "abcd", "Jasvir", "Boparoy")

    # Testing lettered and numerical password < 6 character
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "ab123", "Jasvir", "Boparoy")
    
    # Testing numbers, capital and lowercase letter password < 6 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "Aa1Bb", "Jasvirb", "Boparoy")
    
    # Testing special characters < 6 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "@@@@/", "Jasvir", "Boparoy")
    
    # Testing a combination of characters < 6 characters in length
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "A1b@", "Jasvir", "Boparoy")


# name_first is not between 1 and 50 characters in length
def test_auth_register_invalid_first():
    requests.post(f"{BASE_URL}/workspace/reset"

    # Test for name_first with 0 character
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "", "Boparoy")

    # Test for name_first with 51 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "J" * 51, "Boparoy")

    # Test for name_first with 100 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "J" * 100, "Boparoy")


# name_last is not between 1 and 50 characters in length
def test_auth_register_invalid_last():
    requests.post(f"{BASE_URL}/workspace/reset"

    # Test for name_last with 0 character
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "")
    
    # Test for name_last with 51 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "B" * 51)
    
    # Test for name_last with 100 characters
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "B" * 100)


# Combination of incorrectly entered values (e.g. multiple incorrect cases)
def test_auth_register_invalid_combination():
    requests.post(f"{BASE_URL}/workspace/reset"

    # Test for invalid email, password, first and last name
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("@", "1234", "", "B" * 51)
    
    # Test for invalid password and first name
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123", "J" * 100, "Boparoy")
    
    # Test for invalid names
    with pytest.raises(HTTPError) as e:
        Helper.auth_register("johnsmith@gmail.com", "123456Jasvir", "", "N" * 51)

