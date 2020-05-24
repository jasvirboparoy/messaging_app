import pytest
from src.error import InputError, AccessError
from src.channels import channels_create
from src.channel import channel_invite, channel_messages
from src.auth import auth_register
from src.message import message_send
from src.workspace import reset_workspace
# This file contains tests for channel_messages function

# This function has the following properties:
# INPUT: (token, channel_id, start)
# OUTPUT: {messages, start, end}

# Assumptions:
# Assumes channels_create, channel_invite, channel_messages, auth_register
# and message_send work

# CASES:

# Creates a list of users (each being a dictionary)
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

# Channel id is not a valid channel
def test_channel_messages_invalid_channel(get_5_new_users):
    # Get 5 new users in a list using fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])
    channel_invite(user_1['token'], channel_id, user_5['u_id'])
    
    # Send one message from user_1
    message_send(user_1['token'], channel_id, "Hey everyone, welcome to the channel!")

    # Assume channel_id of 222124 is invalid/not created
    with pytest.raises(InputError) as e:
        channel_messages(user_3['token'], 222124, 0)

    # Assume channel_id of 9898 is invalid/not created
    with pytest.raises(InputError) as e:
        channel_messages(user_3['token'], 9898, 0)
    
    reset_workspace()

# Start is greater than the total number of messages in the channel
def test_channel_messages_invalid_start(get_5_new_users):
    # Get 5 new users in a list using a fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])
    channel_invite(user_1['token'], channel_id, user_5['u_id'])
    
    # Send one message from user_1
    message_send(user_1['token'], channel_id, "Hey everyone, welcome to the channel!")

    # user_2 checks messages
    with pytest.raises(InputError) as e:
        channel_messages(user_2['token'], channel_id, 1)

    # user_3 checks messages
    with pytest.raises(InputError) as e:
        channel_messages(user_3['token'], channel_id, 5)

    # user_4 checks messages
    with pytest.raises(InputError) as e:
        channel_messages(user_4['token'], channel_id, 10)
    
    # user_5 checks messages
    with pytest.raises(InputError) as e:
        channel_messages(user_5['token'], channel_id, 50)
    reset_workspace()

    reset_workspace()

# Authorised user is not a member of channel with channel id
def test_channel_messages_not_member(get_5_new_users):
    # Get 5 new users in a list using a fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_3 as the owner and call it "Standups"
    standups_channel = channels_create(user_3['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_3 token 
    channel_invite(user_3['token'], channel_id, user_1['u_id'])
    channel_invite(user_3['token'], channel_id, user_2['u_id'])
    
    # Send one message from user_1
    message_send(user_2['token'], channel_id, "Hey everyone, welcome to the channel!")

    # User 4 is not an authorised user
    with pytest.raises(AccessError) as e:
        channel_messages(user_4['token'], channel_id, 0)
    
    # User 5 is not an authorised user
    with pytest.raises(AccessError) as e:
        channel_messages(user_5['token'], channel_id, 0)

    reset_workspace()


# Tests the successful case of function
def test_channel_messages_success(get_5_new_users):
     # Get 5 new users in a list using a fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])
    channel_invite(user_1['token'], channel_id, user_5['u_id'])
    
    # Create an empty list that will store dictionaries containing message_id
    message = []

    # Send 75 messages in total, 15 from each user
    for i in range(0, 15):
        message.insert(0, message_send(user_1['token'], channel_id, "Hey everyone!!!"))
        message.insert(0, message_send(user_2['token'], channel_id, "Hey :)!"))
        message.insert(0, message_send(user_3['token'], channel_id, "Keeeeen!"))
        message.insert(0, message_send(user_4['token'], channel_id, "Heyo"))
        message.insert(0, message_send(user_5['token'], channel_id, "YOOOOO"))
    call_1_messages = channel_messages(user_4['token'], channel_id, 0)
    
    # Assert the known details
    assert call_1_messages['start'] == 0
    assert call_1_messages['end'] == 50
    assert call_1_messages['messages'][0]['message_id'] == message[74]['message_id']
    assert call_1_messages['messages'][0]['u_id'] == user_5['u_id']
    assert call_1_messages['messages'][0]['message'] == "YOOOOO"

    call_2_messages = channel_messages(user_4['token'], channel_id, call_1_messages['end'])
    assert call_2_messages['start'] == 50
    assert call_2_messages['end'] == -1
    assert call_2_messages['messages'][0]['message_id'] == message[50]['message_id']

    reset_workspace()
