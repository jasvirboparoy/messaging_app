'''
Full system test 2 for Flask Slackr Server
'''
import urllib
import json
import pytest
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
    def urlopen_users_all(token):

        queryString = urllib.parse.urlencode({
                "token" : token
            })
        response = requests.get(f"{BASE_URL}/users/all?{queryString}")
        payload = response.json()
        return payload
