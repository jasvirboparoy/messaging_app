import pytest
import init_data
from src.channels import channels_create
from src.error import InputError, AccessError
from src.auth import auth_register, is_token_valid
from src.workspace import reset_workspace
from src.standup import standup_send, standup_active, standup_start
from datetime import datetime, timezone
from datetime import timedelta

## Assumptions

## Alter or might not need this
@pytest.fixture
def get_5_new_users():
    # reset_workspace()
    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")

    user_list = [user_1, user_2, user_3, user_4, user_5]
    return user_list

@pytest.fixture
def get_5_lengths():
    # Time lengths in seconds
    reset_workspace()
    length_min = 1800 
    length_hour = 3600 
    length_2hour = 7200
    length_neg = -1111

    length_list = [length_min, length_hour, length_2hour, length_neg]

    return length_list

# @pytest.fixture
# # Creating channels
# def get_channel(get_5_new_users):
#     # Get token
#     user_list = get_5_new_users
#     token1 = user_list[0]["token"]
#     token2 = user_list[1]["token"]

#     # Create public channel
#     channel_pub = channels_create(token1, "channel_pub", True)

#     # Create private channel
#     channel_priv = channels_create(token2, "channel_priv", False)

#     channel_list = [channel_pub, channel_priv]

#     return channel_list

def test_invalid_channel(get_5_lengths):
    
    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")

    assert is_token_valid(user_1['token'])

    length_list = get_5_lengths

    #assume -1111 is an invalid channel_id
    invalid_channel_id = -1111

    with pytest.raises(InputError) as e:
        standup_start(user_1['token'], invalid_channel_id, length_list[0])

    with pytest.raises(InputError) as e:
        standup_start(user_2['token'], invalid_channel_id, length_list[1])

    with pytest.raises(InputError) as e:
        standup_start(user_3['token'], invalid_channel_id, length_list[2])
    
    with pytest.raises(InputError) as e:
        standup_start(user_4['token'], invalid_channel_id, length_list[3])
    reset_workspace()

# def test_standup_active(get_5_lengths):
#     # Get a token
#     user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
#     token = user_1['token']

#     # Get arguments
#     # channel = get_channel[0]
#     c_id = channels_create(token, "tester", True)
#     length = get_5_lengths[1]

#     if not standup_active(token, c_id) is None:
#         with pytest.raises(InputError) as e:
#             standup_start(token, c_id, length)

#     reset_workspace()

def test_time_finish(get_5_lengths):
    # Otain data
    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")
    
    token = user_2['token']

    channel = channels_create(token, "Test", False)
    # length is one hour
    length = get_5_lengths[1]

    # Calculate correct expected time_finish
    time_finish = datetime.timestamp(datetime.now() + timedelta(seconds=length))
    
    # Call standup_start
    time_finish_dict = standup_start(token, channel['channel_id'], length)
    assert time_finish_dict['time_finish'] == time_finish

    reset_workspace()

# def test_invalid_length(get_5_new_users, get_channel, get_5_lengths):
#     # Otain data
#     token = get_5_new_users[0]["token"]
#     channel = get_channel[0]

#     # Get invalid length
#     invalid_length = get_5_lengths[4]

#     # Assert that standup_start returns an error
#     with pytest.raises(InputError) as e:
#         standup_start(token, channel, invalid_length)

#     reset_workspace()

# def test_start_test(get_5_new_users, get_5_lengths):
#     reset_workspace()
#     # Register a user 
#     # users = get_5_new_users
#     user = auth_register("harrypotter@gmail.com", "3534954658kT", "Harry", "Potter")
#     u_id = user["u_id"]
#     token = user["token"]

#     # User 1 create a channel
#     c_id = channels_create(token, "Standup_channel", True)

#     # Get length
#     length = get_5_lengths[2]

#     # User 1 starts a stand up
#     time_finish['time_finish'] = standup_start(token, c_id, length)

#     # Calculate correct expected time_finish
#     time_finish = datetime.timestamp(datetime.now() + timedelta(seconds=length))

#     # Check that CHANNELS.DICT is updated
#     assert init_data.CHANNELS_DICT[c_id]["is_standup"]

#     # Check that channel is added into STANDUP_DICT
#     result = 0
#     for key in init_data.STANDUP_DICT:
#         if c_id == key:
#             result = 1
#     assert result == 1
    
#     # Check that STANDUP.DICT is updated
#     assert init_data.STANDUP_DICT[c_id]["starter_token"] == token
#     assert init_data.STANDUP_DICT[c_id]["time_finsh"] == time_finish

#     reset_workspace()