import pytest
from src.error import InputError, AccessError
from src.channel import channel_invite, channel_join, channel_details, channel_leave, channel_removeowner
from src.channels import channels_create, channels_list
from src.auth import auth_register
from src.workspace import reset_workspace

    
# Tests the functionality of function channels_list

# ASSUMPTIONS
# assumes that auth_register works
# assumes that channels_create, channel_invite, channel_join
# channel_leave, channel_removeowner works
# assume that "associated channel detail" is the channel_id
# and name

def test_list_create_public():
    reset_workspace()
    # testing that channel_list returns channel name and details after
    # public channel is created
    
    # Register user 1
    results = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token = results['token']
    
    # Create a channel
    channel = channels_create(token, "hello_world", True)
    c_id = channel["channel_id"]

    # Call channels_list function
    # channels = channels_list(token)
    
    # Check channels_list returns public channels created
    assert channels_list(token)["channels"][0]['channel_id'] == c_id

    reset_workspace()

    reset_workspace()

def test_list_create_private():
    reset_workspace()
    # testing that channel_list returns channel name and details after
    # private channel is created
    
    # Register user and get token
    results = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token = results["token"]

    # Create a private channel
    channel = channels_create(token, " hello_world", False)
    c_id = channel["channel_id"]
    
    channels = channels_list(token)

    # Check channels_list returns private channels created
    assert channels["channels"][0]['channel_id'] == c_id

    reset_workspace()

def test_list_join_public():
    reset_workspace()
    # testing that channel_list returns channel name and details of
    # if user joins a public channel created by another user
    
    # Register user 1
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]
    
    # Regsiter user 2
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results2["token"]

    # Create public channel
    channel = channels_create(token1, " hello_world", True)
    c_id = channel["channel_id"]

    # User 2 joins public channel
    channel_join(token2, c_id)
    
    channels = channels_list(token2)
    
    # Check channels_list returns public channels created
    assert channels["channels"][0]['channel_id'] == c_id

    reset_workspace()

def test_list_invite_private():
    reset_workspace()
    # testing that channel_list returns channel name and details of
    # if user joins a private channel created by another user

    # User 1 registers
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]

    # User 2 registers
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results2["token"]
    u_id2 = results2["u_id"]

    # Private channel is created
    channel = channels_create(token1, " hello_world", False)
    c_id = channel["channel_id"]

    # User 2 is invited to join the private channel
    channel_invite(token1, c_id, u_id2)
    
    # Call channels_list function
    channels = channels_list(token2)
    
    # Check that list returns the private channel that user 2 was invited to
    assert channels["channels"][0]['channel_id'] == c_id

    reset_workspace()

def test_list_invite_public():
    # testing that channel_list returns channel name and details of
    # if user joins a public channel they were invited to
    reset_workspace()

    # Register user 1
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]

    # Register user 2
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results2["token"]
    u_id2 = results2["u_id"]

    # Create a public channel
    channel = channels_create(token1, " hello_world", True)
    c_id = channel["channel_id"]
    
    # Invite user 2 to a public channel
    channel_invite(token1, c_id, u_id2)
    
    # Call channels_list function
    channels = channels_list(token2)
    
    # Check that channels_list returns channel that user 2 was invited to
    assert channels["channels"][0]['channel_id'] == c_id

    reset_workspace()

def test_join_leave():
    reset_workspace()
    # testing that channel_list returns channel name and details of
    # if user joins a channel and then leaves it

    # user 1 registers to slackr
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
	
    token1 = results1["token"]

    # user 2 registers to slackr
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results1["token"]
    u_id2 = results2["u_id"]

    # channel 1 is created by user 1 and user 2 is invited
    channel1 = channels_create(token1, "hello_world", True)
    c_id1 = channel1["channel_id"]
    channel_invite(token1, c_id1, u_id2)

    # channel 2 is created by user 1 and user 2 joins
    channel2 = channels_create(token1, "channel_2", True)
    c_id2 = channel2["channel_id"]
    channel_invite(token1, c_id2, u_id2)

    # user 2 leaves channel 1
    channel_leave(token1, c_id1)
	
    # test channel_list only lists channel 2 for user 2
    channels = channels_list(token2)
    assert channels["channels"][0]['channel_id'] == c_id2

    reset_workspace()

def test_list_removeowner():
    reset_workspace()
    # testing that channel_list returns channel name and details of
    # if user is removed from a channel

    # user 1 registers to slackr
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]
    u_id1 = results1["u_id"]

    # user 2 registers to slackr
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results1["token"]
    u_id2 = results2["u_id"]

    # channel 1 is created by user 1 and user 2 is invited
    channel1 = channels_create(token1, "channel_1", True)
    c_id1 = channel1["channel_id"]
    channel_invite(token1, c_id1, u_id2)

    # channel 2 is created by user 1 and user 2 joins
    channel2 = channels_create(token1, "channel_2", True)
    c_id2 = channel2["channel_id"]
    channel_invite(token1, c_id2, u_id2)

    # user 2 is removed from channel 1
    channel_removeowner(token2, c_id1, u_id1)
	
    # test channel_list only lists channel 2 for user 2
    channels = channels_list(token2)
    assert channels["channels"][0]['channel_id'] == c_id2

    reset_workspace()

def test_channel_list():
    reset_workspace()
    # testing that channel_list list of all channels that user is in

    # user 1 registers to slackr
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]
    u_id1 = results1["u_id"]

    # user 2 registers to slackr
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results2["token"]
    u_id2 = results2["u_id"]

    # assert u_id2 == channels_list(token2)

    # Adding user 2 to 3 channels
    # user 1 creates a private channel that user 2 is not part of
    channel1 = channels_create(token1, "channel_1", False)
    c_id1 = channel1["channel_id"]

    # user 1 creates a public channel and user 2 joins
    channel2 = channels_create(token1, "channel_2", True)
    c_id2 = channel2["channel_id"]
    channel_join(token2, c_id2)

    # user 1 creates a private channel and invites user 2
    channel3 = channels_create(token1, "channel_3", False)
    c_id3 = channel3["channel_id"]
    channel_invite(token1, c_id3, u_id2)

    # user 2 create a private channel
    channel4 = channels_create(token2, "channel_4", False)
    c_id4 = channel4['channel_id']

    # list of channels that are expected for user 2 to be in
    channels_id = [c_id2, c_id3, c_id4]

    # check channel_list return is correct
    channels = channels_list(token2)["channels"]

    
    result = 0
    for idx in channels:
        result += 1

    assert result == 3

    
    result = 0
    for c_id in channels_id:
        for channel in range(len(channels)):
            if c_id == channels[channel]["channel_id"]:
                result = result + 1
    
    assert result == 3
    
    reset_workspace()