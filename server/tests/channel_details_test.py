import pytest
from src.error import InputError, AccessError
from src.channels import channels_create
from src.channel import channel_details, channel_invite
from src.auth import auth_register
from src.workspace import reset_workspace

# This file contains tests for testing channel_details function

# This function has the following propertites
# INPUT: (token, channel_id)
# OUTPUT: {name, owner_members, all_member}

# Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel

# Assumptions:
# Assume auth_register works, channel_invite works, channel_create works, 
# and errors work (InputError and AccessError)

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

# CASES:

# Channel ID is not a valid channel
def test_channel_details_invalid_channelID(get_5_new_users):
    users_all = get_5_new_users

    token_1 = users_all[0]['token']

    # Assume this channel id is an invalid channel id (i.e hasn't been used)
    channel_id = 2224

    # Attempt to get details of channel that doesn't exist
    with pytest.raises(InputError) as e:
        channel_details(token_1, channel_id)

    reset_workspace()   

# Authorised user is not a member of channel with channel_id
def test_channel_details_unauthorised(get_5_new_users):

    # assign variable to list of 5 users created from auth register
    users_all = get_5_new_users

    # Assign each element in users_all list to user
    user_1 = users_all[0]
    user_2 = users_all[1]
    user_3 = users_all[2]
    user_4 = users_all[3]
    user_5 = users_all[4]

    # Create a private channel called tester using user_1 token
    test_channel = channels_create(user_1['token'], "Tester", False)

    # Attempt to get details of channel using user_2 token (who is not part of channel)
    with pytest.raises(AccessError) as e:
        channel_details(user_2['token'], test_channel['channel_id'])

    # Attempt to get details of channel using user_3 token (who is not part of channel)
    with pytest.raises(AccessError) as e:
        channel_details(user_3['token'], test_channel['channel_id'])

    # Attempt to get details of channel using user_4 token (who is not part of channel)
    with pytest.raises(AccessError) as e:
        channel_details(user_4['token'], test_channel['channel_id'])

    # Attempt to get details of channel using user_5 token (who is not part of channel)
    with pytest.raises(AccessError) as e:
        channel_details(user_5['token'], test_channel['channel_id'])
    
    reset_workspace()

def test_channel_details_success(get_5_new_users):
    
    users_all = get_5_new_users

    user_1 = users_all[0]
    user_2 = users_all[1]
    user_3 = users_all[2]

    # Create a private channel called tester using user_1 token
    test_channel = channels_create(user_1['token'], "Tester", False)

    # Add user_2 and user_3 to private channel
    channel_invite(user_1['token'], test_channel['channel_id'], user_2['u_id'])
    channel_invite(user_1['token'], test_channel['channel_id'], user_3['u_id'])

    # Get channel details
    details = channel_details(user_1['token'], test_channel['channel_id'])

    # Assert name given from channel details matches name of channel
    assert details['name'] == "Tester"

    # Lists of expected details
    expected_owners_u_ids = [user_1['u_id']]
    expected_owners_token = [user_1['token']]
    expected_all_members_u_ids = [user_1['u_id'], user_2['u_id'], user_3['u_id']]
    expected_all_members_tokens = [user_1['token'], user_2['token'], user_3['token']]

    all_members = details['all_members']
    owner_members = details['owner_members']

    # Check if owner member u_id is correct
    owner_members_u_ids = [member['u_id'] for member in owner_members]
    assert owner_members_u_ids.sort() == expected_owners_u_ids.sort()

    # Check if owner member token is correct
    # owner_members_tokens = [member['token'] for member in owner_members]
    # assert owner_members_tokens.sort() == expected_owners_token.sort()

    # Check if all members u_id is correct
    all_members_u_ids = [member['u_id'] for member in all_members]
    assert all_members_u_ids.sort() == expected_all_members_u_ids.sort()

    # Check if all members token is correct
    # all_members_tokens = [member['token'] for member in all_members]
    # assert all_members_tokens.sort() == expected_all_members_tokens.sort()

    reset_workspace()
