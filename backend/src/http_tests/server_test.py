"""
Full system test 1 for Flask Slackr Server
"""
import urllib
import json
import pytest
import requests

BASE_URL = 'http://127.0.0.1:5390'

#@pytest.mark.parametrize("earned,spent,expected", [
#    (30, 10, 20),
#    (20, 2, 18),
#])
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
    def urlopen_users_all(token):

        queryString = urllib.parse.urlencode({
                "token" : token
            })
        response = requests.get(f"{BASE_URL}/users/all?{queryString}")
        payload = response.json()
        return payload


def test_server_system_1():
    """
    Generic system test
    """

    requests.post(f"{BASE_URL}/workspace/reset")
    users = [None,None,None,None,None]
    # Register 5 users
    users[0] = Helpers.urlopen_register("johnsmith@gmail.com", "jpass123", "John", "Smith")
    users[1] = Helpers.urlopen_register("henrysmith@gmail.com", "hpass123", "Henry", "Smith")
    users[2] = Helpers.urlopen_register("jimhenry@gmail.com", "jhpass123", "Jim", "Henry")
    users[3] = Helpers.urlopen_register("henryford@gmail.com", "hjpass123", "Henry", "Ford")
    users[4] = Helpers.urlopen_register("jamestownsend@gmail.com", "jtpass123", "James", "Townsend")

    # check user_all to assert all users are registered
    users_all = Helpers.urlopen_users_all(users[0]["token"])
    assert len(users) == len(users_all["users"])

    # check u_ids are matching
    shown_u_ids = []
    for user_shown in users_all["users"]:
        shown_u_ids.append(user_shown["u_id"])
    
    for user in users:
        assert user["u_id"] in shown_u_ids


    # Users Logout
    user_logout = [None]*5
    user_logout[0] = Helpers.urlopen_logout(users[0]["token"])
    user_logout[1] = Helpers.urlopen_logout(users[1]["token"])
    user_logout[2] = Helpers.urlopen_logout(users[2]["token"])
    user_logout[3] = Helpers.urlopen_logout(users[3]["token"])
    user_logout[4] = Helpers.urlopen_logout(users[4]["token"])

    for user in user_logout:
        assert user["is_success"] == True



