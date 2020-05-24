''' This file contains the tests for admin_user_remove function '''
import pytest
from src.admin import admin_user_remove, admin_userpermissions_change
from src.auth import auth_register
from src.channel import (channel_messages, channel_details, channel_join,
                         is_u_id_valid, is_token_valid)
from src.channels import channels_create
from src.error import AccessError, InputError
from src.message import message_send
from src.user import user_profile
from src.users import users_all
from src.workspace import reset_workspace


# Function to be tested:
# admin_user_remove
# Input: (token, u_id)
# Output: {}

@pytest.fixture
def register_5_new_users():
    ''' Registers 5 new users to system '''
    reset_workspace()

    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")

    user_list = [user_1, user_2, user_3, user_4, user_5]

    return user_list

def test_remove_invalid_user(register_5_new_users):
    ''' Attempt to remove invalid user - input error'''
    users = register_5_new_users

    admin_token = users[0]["token"]

    # Assume 1 is not a valid u_id
    with pytest.raises(InputError) as e:
        admin_user_remove(admin_token, -1)

    # Actually remove the user here
    admin_user_remove(admin_token, users[1]["u_id"])

    # Attempt to remove user[1] again
    with pytest.raises(InputError) as e:
        admin_user_remove(admin_token, users[1]["u_id"])

    # Check user_all
    user_list = users_all(users[0]['token'])

    removed_u_id = users[1]["u_id"]

    u_ids = [user["u_id"] for user in user_list['users']]

    assert removed_u_id not in u_ids

    reset_workspace()

def test_invalid_permission_remove(register_5_new_users):
    '''
    Attempt to remove user with account that
    doesn't have correct permissions
    '''
    users = register_5_new_users

    unauthorised_token = users[1]["token"]
    with pytest.raises(AccessError) as e:
        admin_user_remove(unauthorised_token, users[0]["u_id"])

    reset_workspace()

def test_success_case(register_5_new_users):
    ''' Tests the success case '''
    users_list = register_5_new_users
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]

    # user_1 gives user_2 admin rights
    admin_userpermissions_change(user_1['token'], user_2['u_id'], 1)

    # user_2 removes user_3
    admin_user_remove(user_2['token'], user_3['u_id'])

    # Assert user_1 and user_2 in users_all, and user_3 is not in users_all
    # This function returns a list of dictionaries
    all_users = users_all(user_2['token'])

    # Make a list containing all the u_ids
    all_users_uids = [user['u_id'] for user in all_users['users']]

    assert user_1['u_id'] in all_users_uids
    assert user_2['u_id'] in all_users_uids
    assert user_3['u_id'] not in all_users_uids

    reset_workspace()

def test_remove_in_channel(register_5_new_users):
    '''
    Tests case of removing user when they are
    part of a channel and have already sent messages
    '''
    # register 3 users and create public channel, where 2 members join
    users = register_5_new_users
    token1 = users[0]["token"]
    token2 = users[1]["token"]
    token3 = users[2]["token"]

    # User 3 creates a public channel
    channel_id = channels_create(token3, "testchannel", True)
    c_id = channel_id["channel_id"]
    # Users 2 and 1 join the channel
    channel_join(token2, c_id)
    channel_join(token1, c_id)

    # send 3 messages
    message_send(token3, c_id, "test1")
    message_send(token2, c_id, "test2")
    message_send(token1, c_id, "test3")

    # remove user3
    user3_uid = users[2]["u_id"]
    admin_user_remove(token1, user3_uid)

    # check channel_messages has 3 messages
    messages = channel_messages(token1, c_id, 0)
    assert len(messages) == 3

    # check channel_details
    c_details = channel_details(token1, c_id)

    # check length of channel members lists
    assert len(c_details["owner_members"]) == 0
    assert len(c_details["all_members"]) == 2

    reset_workspace()

def test_user_profiles_correct(register_5_new_users):
    ''' Checks that user profile is no longer in system '''

    # Register 4 users
    users_list = register_5_new_users
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]

    # User 4 is removed by user 1
    admin_user_remove(user_1['token'], user_4['u_id'])

    # Assert that user 4’s is no longer valid user/logged out now
    # assert not is_u_id_valid(user_4['u_id'])
    assert not is_token_valid(user_4['token'])

    all_users_list = users_all(user_1['token'])

    # Make a list containing all the u_ids
    all_users_uids = [user['u_id'] for user in all_users_list['users']]

    # Assert users_all only shows remaining 3 users
    assert user_1['u_id'] in all_users_uids
    assert user_2['u_id'] in all_users_uids
    assert user_3['u_id'] in all_users_uids
    assert user_4['u_id'] not in all_users_uids

    # Assert user_profile returns input error
    # Not sure if this is true yet??
    with pytest.raises(InputError) as e:
        user_profile(user_1['token'], user_4['u_id'])

    reset_workspace()
