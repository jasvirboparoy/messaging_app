import pytest
from src.error import InputError
from src.channel import channel_join
from src.channels import channels_create
from src.workspace import reset_workspace
import urllib
from urllib.error import HTTPError
import json
import pytest
import requests

BASE_URL = 'http://127.0.0.1:5390'
# testing the general functionality of channels create - can it create 
# a normal channel and then is it possible to join the channel - tests
# assumes auth_register works 
# assumes channel_join works

class Helper:
    """
    test class containg helper functions
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
    def channels_create(token,name,is_public):
        """
        Testing Wrapper to open /channels/create for a given email,
        Input: token,name,is_public
        Output: { channel_id }
        """

        data = json.dumps({
            "token" : token,
            "name" : name,
            "is_public" : is_public
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/channels/create",
            data=data,
            headers={'Content-Type': 'application/json'} )
        payload = json.load(urllib.request.urlopen(req))

        return payload

    @staticmethod
    def channel_invite(token, channel_id, u_id):

        data = json.dumps({
            "token" : token,
            "channel_id" : channel_id,
            "u_id" : u_id
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/channel/invite",
            data=data,
            headers={'Content-Type': 'application/json'} )
        payload = json.load(urllib.request.urlopen(req))

        return payload

    @staticmethod
    def channel_join(token, channel_id):

        data = json.dumps({
            "token" : token,
            "channel_id" : channel_id,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{BASE_URL}/channel/join",
            data=data,
            headers={'Content-Type': 'application/json'} )
        payload = json.load(urllib.request.urlopen(req))

        return payload

def test_channels_create():
    # assume that channel_join works, and channel is public
    requests.post(f"{BASE_URL}/workspace/reset"
    results = Helper.auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = Helper.channels_create(results["token"],"testchannel",True)

    Helper.channel_join(results["token"], c_id["channel_id"])

# assume channels will not be able to created with same name
def test_channels_create_double():
    requests.post(f"{BASE_URL}/workspace/reset"
    results = Helper.auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = Helper.channels_create(results["token"],"testchannel2",False)

    with pytest.raises(InputError) as e:
        Helper.channels_create(results["token"],"testchannel2",False)

    with pytest.raises(InputError) as e:
        Helper.channels_create(results["token"],"testchannel2",True)

# assume created public channels will not be able to be created with same 
# name as created private channel and vice versa

def test_channels_create_double2():
    requests.post(f"{BASE_URL}/workspace/reset"
    results = Helper.auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = Helper.channels_create(results["token"],"testchannel3",True)
    with pytest.raises(InputError) as e:
        Helper.channels_create(results["token"],"testchannel3",False)

def test_channels_create_double3():
    requests.post(f"{BASE_URL}/workspace/reset"
    results = Helper.auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = Helper.channels_create(results["token"],"testchannel4",True)
    with pytest.raises(InputError) as e:
        Helper.channels_create(results["token"],"testchannel4",True)


# function is testing failures for create channel -  
def test_create_fails():
    requests.post(f"{BASE_URL}/workspace/reset"
    results1 = Helper.auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    # testing a channel with name more then 20 characters
    #1
    with pytest.raises(InputError) as e:
        Helper.channels_create(results1["token"], "a" * 21, True)
    #2 longer
    with pytest.raises(InputError) as e:
        Helper.channels_create(results1["token"], "a" * 1000, True)
    #3 special characters
    with pytest.raises(InputError) as e:
        Helper.channels_create(results1["token"], "!" * 21, True)
    #3 spaces
    with pytest.raises(InputError) as e:
        Helper.channels_create(results1["token"], " " * 21, True)
    