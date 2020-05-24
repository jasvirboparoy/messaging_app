import pytest
import init_data
from src.error import InputError, AccessError
from src.channel import channel_addowner, channel_leave,channel_invite, channel_join
from src.channels import channels_create, channels_list
from src.auth import auth_register
from src.workspace import reset_workspace

# ASSUMPTIONS
# assumes that channel_list and channel_listall work
# assumes that channel_join works
# assumes that auth_registers works

@pytest.fixture
def get_5_new_users():

    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")

    user_list = [user_1, user_2, user_3]
    return user_list

# Test InputErrors in channel_leave
def test_input_errors(get_5_new_users):
    # Register user
    u_id1 = get_5_new_users[0]["u_id"]
    token1 = get_5_new_users[0]["token"]

    # Assume -1111 is an invalid channel_id
    invalid_channel_id = -1111

    # Check that channel_leave throws error
    with pytest.raises(InputError) as e:
        channel_join(token1, invalid_channel_id)

    reset_workspace()

# Test the AccessErrors in channel_leave
def test_input_errors(get_5_new_users):
    # Register user 1 and create channel 1
    token1 = get_5_new_users[0]["token"]
    c_id1 = channels_create(token1, "Channel1", True)["channel_id"]

    # Register user 2
    token2 = get_5_new_users[1]["token"]

    # Check that channel_leave throws AccessError when user 2 leaves channel 1
    with pytest.raises(AccessError) as e:
        channel_leave(token2, c_id1)

    reset_workspace()

# Test that owner can succesfully leave a channel
def test_channel_leave_owner(get_5_new_users):
    # Register user 1 and user 1 creates a public channel. User 1 is an ownder
    u_id1 = get_5_new_users[0]["u_id"]
    token1 = get_5_new_users[0]["token"]
    c_id1 = channels_create(token1, "Channel1", True)["channel_id"]
    
    # Register user 2. User 1 invites user 2 as an to Channel1
    u_id2 = get_5_new_users[1]["u_id"]
    token2 = get_5_new_users[1]["token"]
    channel_invite(token1, c_id1, u_id2)

    # Checking that user 1 is an owner in system
    owners_list = init_data.CHANNELS_DICT[c_id1]["owners"]
    result = 0
    for key in owners_list:
        if key["u_id"] == u_id1:
            result = 1
    assert result == 1  

    # User 1 leaves Channel1 
    channel_leave(token1, c_id1)

    # Check that user 1 is successfully removed from owners list in CHANNELS_DICT with channel_leave  
    result = 0
    for key in owners_list:
        if key["u_id"] == u_id1:
            result = 1
    assert result == 0

    # Check that user 1 is successfully removed from members list in CHANNELS_DICT with channel_leave
    members_list = init_data.CHANNELS_DICT[c_id1]["members"]
    result = 0
    for key in members_list:
        if key["u_id"] == u_id1:
            result = 1
    assert result == 0
    reset_workspace()

# Test channel is deleted if the last member in the channel leaves
def test_channel_leave_delete(get_5_new_users):
    # Register user 1 and user 1 creates a public channel. User 1 is an ownder
    u_id1 = get_5_new_users[0]["u_id"]
    token1 = get_5_new_users[0]["token"]
    c_id1 = channels_create(token1, "Channel1", True)["channel_id"]

    # User 1 leaves Channel1 
    channel_leave(token1, c_id1)

    # Check that channel is deleted from CHANNEL_DICT
    channels = init_data.CHANNELS_DICT
    
    result = 0
    for key in channels:
        if key == c_id1:
            result = 1
    assert result == 0
    reset_workspace()

# Test the AccessErrors in channel_leave
def test_channel_leave_addowner(get_5_new_users):
    # Register user 1 and user 1 creates a public channel. User 1 is an ownder
    token1 = get_5_new_users[0]["token"]
    c_id1 = channels_create(token1, "Channel1", True)["channel_id"]
    
    # Register user 2. User 1 adds user 2 as an owner of Channel1
    u_id2 = get_5_new_users[1]["u_id"]
    token2 = get_5_new_users[1]["token"]
    channel_invite(token1, c_id1, u_id2)
    channel_addowner(token1, c_id1, u_id2)

    # Checking that user 2 has been added as an owner
    owners_list = init_data.CHANNELS_DICT[c_id1]["owners"]
    result = 0
    for key in owners_list:
        if key["u_id"] == u_id2:
            result = 1
    assert result == 1  

    # User 2 leaves Channel1 
    channel_leave(token2, c_id1)

    # Check that user 2 is successfully removed from owners list in CHANNELS_DICT with channel_leave  
    result = 0
    for key in owners_list:
        if key["u_id"] == u_id2:
            result = 1
    assert result == 0

    # Check that user 2 is successfully removed from members list in CHANNELS_DICT with channel_leave
    members_list = init_data.CHANNELS_DICT[c_id1]["members"]
    result = 0
    for key in members_list:
        if key["u_id"] == u_id2:
            result = 1
    assert result == 0
    reset_workspace()

# Test that member can leave channel
def test_channel_leave_member(get_5_new_users):
    # Register user 1 and user 1 creates a public channel. User 1 is an ownder
    token1 = get_5_new_users[0]["token"]
    c_id1 = channels_create(token1, "Channel1", True)["channel_id"]
    
    # Register user 2. User 1 adds user 2 as an owner of Channel1
    u_id3 = get_5_new_users[2]["u_id"]
    token3 = get_5_new_users[2]["token"]
    channel_invite(token1, c_id1, u_id3)

    # User 3 leaves Channel1 
    channel_leave(token3, c_id1)

    # Check that user 2 is successfully removed from members list in CHANNELS_DICT with channel_leave
    members_list = init_data.CHANNELS_DICT[c_id1]["members"]
    result = 0
    for key in members_list:
        if key["u_id"] == u_id3:
            result = 1
    assert result == 0
    reset_workspace()