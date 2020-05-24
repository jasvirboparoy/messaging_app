import pytest
import init_data
from src.channels import channels_create
from src.error import InputError, AccessError
from src.workspace import reset_workspace
from src.auth import auth_register
from src.standup import standup_send, standup_active, standup_start
from datetime import datetime, timezone, timedelta
import threading

## Assumptions

## Alter or might not need this
@pytest.fixture
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
    length_sec = 30

    length_list = [length_min, length_hour, length_2hour, length_neg]

    return length_list

@pytest.fixture
# Creating channels
def get_channel():
    reset_workspace()

    # Get token
    user_list = get_5_new_users()
    token1 = user_list[0]["token"]
    token2 = user_list[1]["token"]

    # Create public channel
    channel_pub = channels_create(token1, "channel_pub", True)
    # Create private channel
    channel_priv = channels_create(token2, "channel_priv", False)

    channel_list = [channel_pub, channel_priv]

    return channel_list

def test_invalid_channel():
    # Get user tokens for arguments
    user_list = get_5_new_users()
    length_list = get_5_lengths()

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

# Message is more than 1000 characters
def test_invalid_message():
    # Obtain arguments data
    token = get_5_new_users()[0]
    channel = get_channel()[0]
    length = get_5_lengths()[0]

    # Create messages over 1000 characters
    invalid_string_1 = "d" * 1001
    invalid_string_2 = "e" * 2000

    # Call standup_start to start standup
    standup_start(token, channel, length)

    # Raises error since message is over 1000 characters
    with pytest.raises(InputError) as e:
        standup_send(token, channel, invalid_string_1)

    with pytest.raises(InputError) as e:
        standup_send(token, channel, invalid_string_2)

# Active standup is not running in the channel
def test_channel_standup():
    # No standup will be started in the channel 
    # Obtain argument data
    token = get_5_new_users()[0]
    channel = get_channel()[0]
    string = "I have completed all my functions"

    # Check that data in CHANNEL_DICT says that no standup exists in the channel
    channels = init_data.CHANNELS_DICT
    assert not channels[channel]["is_standup"]

    # Raise InputError
    with pytest.raises(InputError) as e:
        standup_send(token, channel, string)

# Authorised user is not a member of the channel
def test_user_not_member(get_5_new_users, get_channel):
    # No standup will be started in the channel 
    # Obtain token for user 1
    token = get_5_new_users[0]

    # Obtain channel_id for chanenl_2 whehere user is not a member of 
    channel = get_channel[1]

    # Creat standup message string
    string = "I have not completed all my functions"

    # Raise AccessError
    with pytest.raises(AccessError) as e:
        standup_send(token, channel, string)

# Throws an error if the user calls standup_send past the time_finish
def test_invalid_send_time(get_5_lengths):
    # Obtain argument data
    token = get_5_new_users()[0]
    channel_id = get_channel()[0]
    message = "Sorry I'm late"
    length = get_5_lengths[4] # 30 seconds

    # Create standup
    time_finish = standup_start(token, channel_id, length)

    if datetime.now() > time_finish:
        with pytest.raises(AccessError) as e:
            standup_send(token, channel_id, message)

def test_standup_send(get_5_new_users, get_5_lengths):
    # Register 5 users
    users = get_5_new_users

    # Get standup time length
    length = get_5_lengths[4]

    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")

    # User 1 creates a channel and starts a standup in that channel
    standup_channel = channels_create(users[0]["token"], "standup_channel", True)
    time_finish = standup_start(users[0]["token"], standup_channel, length)

    # User 2 sends a standup 5 seconds after
    time_after2 = 5
    message2 = "I saw a cat."
    thread = threading.Timer(time_after2, standup_send(users[1]["token"], standup_channel, message2))
    thread.start()
    thread.join()
    message_buffer2 = "Henry: " + message2 + "\n"

    # User 3 sends a standup 5 seconds after
    time_after3 = 10
    message3 = "It can down the stairs "
    thread = threading.Timer(time_after3, standup_send(users[2]["token"], standup_channel, message3))
    thread.start()
    thread.join()
    message_buffer3 = "Jim: " + message3 + "\n"

    # User 4 sends a standup 5 seconds after
    time_after4 = 15
    message4 = "and jumped on the rail. "
    thread = threading.Timer(time_after4, standup_send(users[3]["token"], standup_channel, message4))
    thread.start()
    thread.join()
    message_buffer4 = "Henry: " + message4 + "\n"

    # User 5 sends a standup 5 seconds after
    time_after5 = 20
    message5 = "That made me laugh"
    thread = threading.Timer(time_after5, standup_send(users[4]["token"], standup_channel, message5))
    thread.start()
    thread.join()
    message_buffer5 = "Henry: " + message5 + "\n"

    # Expected message to be in message_buffer
    expected_buffer = message_buffer2 + message_buffer3 + message_buffer4 + message_buffer5

    assert init_data.STANDUP_DICT[standup_channel]["message_buffer"] == expected_buffer

    # Check that message has been sent after time_finish
    length = 30
    thread = threading.Timer(length, check_standup_message_sent(expected_buffer, standup_channel))
    thread.start()
    thread.join()

# Check that when current time has reached time_finish, standup message has been sent
def check_standup_message_sent(expected_buffer, standup_channel):
    assert init_data.MESSAGES_DICT[standup_channel]["message"][0] == expected_buffer
    