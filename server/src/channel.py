'''
This file contains the functions for getting
info about a specific channel
'''
import init_data
from error import AccessError, InputError
from auth import is_token_valid
from channel_helper import is_channel_id_valid, is_user_in_channel, user_channel_permissions
from user_helper import get_u_id, is_u_id_valid

def is_user_owner(u_id, c_id):
    """
    Check user is in an owner
    Input: u_id,c_id
    Output:Boolean
    """ 
    owners_list = init_data.CHANNELS_DICT[c_id]["owners"]
    for key in owners_list:
        if key["u_id"] == u_id:
            return True
    return False

def is_user_idx_owner(u_id, c_id):
    """
    Check user is in an owner
    Input: u_id,c_id
    Output:Boolean
    """ 
    owners_list = init_data.CHANNELS_DICT[c_id]["owners"]
    idx = -1
    for key in owners_list:
        idx += 1
        if key["u_id"] == u_id:
            return idx
    return idx

def is_user_idx_member(u_id, c_id):
    """
    Check user is in an member and get idx in list
    Input: u_id,c_id
    Output:Boolean
    """ 
    members_list = init_data.CHANNELS_DICT[c_id]["members"]
    idx = -1
    for key in members_list:
        idx += 1
        if key["u_id"] == u_id:
            return idx
    return idx

# Jasvir's function below
def channel_details(token, channel_id):
    '''
    Gets channel details of a given channel
    Input: token, channel_id
    Output: {name, owner_members, all_members}
    '''
    # Check if token is valid
    if not is_token_valid(token):
        raise AccessError(description="Invalid token used")

    # Check if channel id is valid
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel id is not a valid channel")

    # Get the data for channel
    name = init_data.CHANNELS_DICT[channel_id]['name']
    owner_members = init_data.CHANNELS_DICT[channel_id]['owners']
    all_members = init_data.CHANNELS_DICT[channel_id]['members']

    # Get the u_id for token
    u_id = get_u_id(token)
    # Find out the user permissions (1 = owner, 2 = member, -1 = not in channel)
    permissions = user_channel_permissions(u_id, channel_id)

    # Raise error if user not in channel
    if permissions['permission_id'] == -1:
        raise AccessError(description="User is not a member of channel")

    return {
        'name': name,
        'owner_members': owner_members,
        'all_members': all_members
        }

def number_of_channel_messages(channel_id):
    '''
    Calculates the total number of messages
    in a channel
    Input: channel_id
    Output: { num_of_messages }
    '''
    messages = init_data.MESSAGES_DICT[channel_id]
    return len(messages)

# Jasvir's function below
def channel_messages(token, channel_id, start):
    '''
    Gets the channel messages (up to 50 at a time)
    Input: token, channel_id, start
    Output: {messages, start, end}
    '''

    u_id = get_u_id(token)

    if not is_user_in_channel(u_id, channel_id):
        raise AccessError(description="User is not in channel")

    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel id is not valid")

    num_messages = number_of_channel_messages(channel_id)

    if start > num_messages:
        raise InputError(description="Start greater than total messages")

    messages = init_data.MESSAGES_DICT[channel_id]

    end = start + 50

    if end >= num_messages:
        end = -1

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

def channel_leave(token, channel_id):
    """
    User leaves the a channel specificed for channel_id
    Input: token, channel_id
    Output: {}
    """
    u_id = get_u_id(token)

    # Raise errors
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel is invalid")
    if not is_user_in_channel(u_id, channel_id):
        raise AccessError(description="User is not part of the channel")
    
    # Check if there is only one member in the channel
    members_list = init_data.CHANNELS_DICT[channel_id]["members"]
    num = 0
    for key in members_list:
        num += 1
    
    # HERE
    # Check if user is an owner 
    # If there is only one member in the channel, delete the channel
    if num == 1:
        del init_data.CHANNELS_DICT[channel_id]
    else:
        # Remove member from owner list
        if is_user_owner(u_id, channel_id):
            owners_list = init_data.CHANNELS_DICT[channel_id]["owners"]
            idx1 = is_user_idx_owner(u_id, channel_id)
            del owners_list[idx1]
        # Remove from member list
        idx2 = is_user_idx_member(u_id, channel_id)
        del members_list[idx2]

    return {
    }

# Ernests function below
def channel_join(token, channel_id):
    """
    User Joins the a channel specificed for channel_id
    Input: token, channel_id, start
    Output: {messages, start, end}
    """

    # AccessError - invalid token
    # Find u_id associated with token
    u_id = get_u_id(token)

    # InputError - c_id is invalid (not in the database)
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel id is not a valid channel")

    # AccessError - when is_public is false (private channel)
    if init_data.CHANNELS_DICT[channel_id]["is_public"] == False:
        raise AccessError(description="Cannot Join private channel")

    if u_id in init_data.CHANNELS_DICT[channel_id]["members"]:
        raise AccessError(description="you are already part of this channel")

    # grab name from u_id
    name_first = init_data.USER_DICT[u_id]["name_first"]
    name_last = init_data.USER_DICT[u_id]["name_last"]
    profile_img_url = init_data.USER_DICT[u_id]["profile_img_url"]

    user = {"u_id":u_id, "name_first":name_first, "name_last":name_last, "profile_img_url":profile_img_url}
    # add u_id to channel
    init_data.CHANNELS_DICT[channel_id]["members"].append(user)
    print (init_data.CHANNELS_DICT)

    return {}

def channel_invite(token, channel_id, u_id):
    """
    invites user with u_id to join channel with channel_id
    Input: token, channel_id, u_id
    Output:
    """

    # Get u_id otherwise 
    # AccessError for invalid token
    authorised_u_id = get_u_id(token)

    # InputError - c_id is invalid (not in the database)
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel id is not a valid channel")

    # Input Error - u_id does not refer to a valid user - check if user exists
    if not is_u_id_valid(u_id):
        raise InputError(description="User is not valid")

    # check if authorised_u_id is already in channel,
    if not is_user_in_channel(authorised_u_id, channel_id):
        raise AccessError(description="You are not in the channel")

    #grab first and last names
    name_first = init_data.USER_DICT[u_id]["name_first"]
    name_last = init_data.USER_DICT[u_id]["name_last"]
    profile_img_url = init_data.USER_DICT[u_id]["profile_img_url"]
    user = {"u_id":u_id, "name_first":name_first, "name_last":name_last, "profile_img_url":profile_img_url}

    # check if user is already in channel, if not do nothing
    if not is_user_in_channel(u_id, channel_id):
        init_data.CHANNELS_DICT[channel_id]["members"].append(user)

    return{}

def channel_addowner(token, channel_id, u_id):
    """
    Make user with user id u_id an owner of this channel
    Input: token, channel_id, u_id
    Output:
    """
    # Retreive u_id otherwise raises error
    user_u_id = get_u_id(token)

    # InputError - Channel ID is not a valid channel
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel id is not a valid channel")
    
    # When user with user id u_id is already an owner of the channel
    # Check u_id against global permissions then channel owner 
    global_p_id = init_data.USER_DICT[u_id]["global_permission_id"]
    if global_p_id == 1 or user_channel_permissions(u_id, channel_id)["permission_id"] == 1:
        raise InputError(description="Added User is already an Owner")

    # AccessError when the authorised user is not an owner of the slackr, or an 
    # owner of this channel
    # Check user_u_id against the global_permission_id and owner list of channel
    global_p_id_user = init_data.USER_DICT[user_u_id]["global_permission_id"]
    channel_p_id_user = user_channel_permissions(user_u_id, channel_id)["permission_id"]
    if global_p_id_user != 1 and channel_p_id_user != 1:
        raise AccessError(description="User is not allowed to add owners")

    # addowner to owner list
    name_first = init_data.USER_DICT[u_id]["name_first"]
    name_last = init_data.USER_DICT[u_id]["name_last"]
    user = {"u_id":u_id, "name_first":name_first, "name_last":name_last}

    init_data.CHANNELS_DICT[channel_id]["owners"].append(user)
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    """
    Remove user with user id u_id an owner of this channel
    Input: token, channel_id, u_id
    Output:
    """
    # Retreive u_id otherwise raises error
    user_u_id = get_u_id(token)

    # InputError - Channel ID is not a valid channel
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel id is not a valid channel")
    
    # When user with user id u_id is not an owner of the channel
    # Check u_id against global permissions then channel owner 
    global_p_id = init_data.USER_DICT[u_id]["global_permission_id"]
    if global_p_id != 1 and user_channel_permissions(u_id, channel_id)["permission_id"] != 1:
        raise InputError(description="User you are trying to remove is not an Owner")

    # AccessError when the authorised user is not an owner of the slackr, or an 
    # owner of this channel
    # Check user_u_id against the global_permission_id and owner list of channel
    global_p_id_user = init_data.USER_DICT[user_u_id]["global_permission_id"]
    channel_p_id_user = user_channel_permissions(user_u_id, channel_id)["permission_id"]
    if global_p_id_user != 1 and channel_p_id_user != 1:
        raise AccessError(description="User is not allowed to remove owners")

    # Remove the owner here

    owners = init_data.CHANNELS_DICT[channel_id]["owners"]
    
    for i in range(len(owners)): 
        if owners[i]["u_id"] == u_id: 
            del owners[i] 
            break

    return {
    }