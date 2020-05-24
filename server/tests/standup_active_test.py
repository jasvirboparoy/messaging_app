import pytest
import init_data
from src.channels import channels_create
from src.error import InputError, AccessError
from src.workspace import reset_workspace
from src.standup import standup_send, standup_active, standup_start
from src.auth import auth_register
from datetime import datetime
from datetime import timedelta

## Assumptions

## Alter or might not need this
""" @pytest.fixture
def get_5_new_users():
    reset_workspace()
    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")

    user_list = [user_1, user_2, user_3, user_4, user_5]
    return user_list

@pytest.fixture
def get_5_lengths():
    reset_workspace()
    # Time lengths in seconds
    length_min = 1800 
    length_hour = 3600 
    length_2hour = 7200
    length_neg = -1111

    length_list = [length_min, length_hour, length_2hour, length_neg]

    return length_list

@pytest.fixture
# Creating channels
def get_channel():
    reset_workspace()

    # Get token
    user_list = get_5_new_users()
    token1 = user_list[0]["token"]
    token2 = user_list[2]["token"]

    # Create public channel
    channel_pub = channels_create(token1, "channel_pub", True)
    # Create private channel
    channel_priv = channels_create(token2, "channel_priv", False)

    channel_list = [channel_pub, channel_priv]

    return channel_list
"""

def test_invalid_channel():
    # Get user tokens for arguments
    """ user_list = get_5_new_users()
    length_list = get_5_lengths()""" 

    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")

    user_list = [user_1, user_2, user_3, user_4, user_5]

    # Create list of user tokens
    tokens = []

    for i in user_list:
        tokens.append(i["token"])

    #assume -1111 is an invalid channel_id
    invalid_channel_id = -1111
    with pytest.raises(InputError) as e:
        standup_start(tokens[0], invalid_channel_id, length_list[0])

    with pytest.raises(InputError) as e:
        standup_start(tokens[1], invalid_channel_id, length_list[1])

    with pytest.raises(InputError) as e:
        standup_start(tokens[2], invalid_channel_id, length_list[2])
    
    with pytest.raises(InputError) as e:
        standup_start(tokens[3], invalid_channel_id, length_list[3])

    reset_workspace()

def test_standup_active_pub():
    # test case where a standup is active on a public channel

    # Obtain data arguments
    # Otain data
    token = get_5_new_users()[0]["token"]
    channel = get_channel()[0]
    length = get_5_lengths()[2]

    # Call standup_start to create a standup
    time_finish = standup_start(token, channel, length)

    # Check that standup_start updates CHANNEL_DICT in data structure 
    channels = init_data.CHANNELS_DICT
    assert channels[channel]["is_standup"]

    # Check that standup_active return is True
    assert standup_active(token, channel) == [True, time_finish]

    reset_workspace()

def test_standup_active_priv():
    # test case where a standup is active on a private channel

    # Obtain data arguments
    # Otain data
    token = get_5_new_users()[0]["token"]
    channel = get_channel()[1]
    length = get_5_lengths()[2]

    # Call standup_start to create a standup
    time_finish = standup_start(token, channel, length)

    # Check that standup_start updates CHANNEL_DICT in data structure 
    channels = init_data.CHANNELS_DICT
    assert channels[channel]["is_standup"] == True

    # Check that standup_active return is True
    assert standup_active(token, channel) == [True, time_finish]

    reset_workspace()

def test_standup_active_none():
    # test case where a no standup exists on a channel
    channel = get_channel()[0]
    token = get_5_new_users()[0]["token"]

    # Check that "is_standup" key in CHANNEL_DICT in data structure is still "False"
    channels = init_data.CHANNELS_DICT
    assert channels[channel]["is_standup"] == False

    # Check that standup_active return is True
<<<<<<< HEAD
    assert standup_active(token, channel) == [False, None]

    reset_workspace()
=======
    assert standup_active(token, channel) == [False, None]
>>>>>>> master
