''' This file contains admin user functions '''
import init_data
from error import InputError, AccessError
from user_helper import is_token_valid, is_u_id_valid, get_u_id, is_user_deleted
from auth import auth_logout

def remove_user_from_channels(u_id):
    '''
    Removes a user from all channels they are part of
    Input: u_id
    Output:
    '''
    # Get a list of the channels a user is part of
    user_channels = channels_list(u_id)
    # Get the channel ids of the channels
    channel_ids = [channel['channel_id'] for channel in user_channels]

    channel_dict = init_data.CHANNELS_DICT

    for c_id in channel_ids:
        for owner in channel_dict[c_id]['owners']:
            if owner['u_id'] == u_id:
                channel_dict[c_id]['owners'].remove(owner)

        for member in channel_dict[c_id]['members']:
            if member['u_id'] == u_id:
                channel_dict[c_id]['members'].remove(member)


def invalidate_user_session(u_id):
    '''
    Terminates a users session
    Input: u_id
    Output: { is_success }
    '''
    valid_tokens_dict = init_data.TOKENS_DICT['valid_tokens']
    for key in valid_tokens_dict:
        if valid_tokens_dict[key] == u_id:
            return auth_logout(key)


def is_permission_id_valid(permission_id):
    '''
    Checks whether permission_id is valid
    Input: permission_id
    Output: Boolean
    '''
    if permission_id == 1 or permission_id == 2:
        return True

    return False

def is_user_owner(token):
    '''
    Checks whether user is an owner
    Input: token
    Output: Boolean
    '''
    u_id = get_u_id(token)

    user_list = init_data.USER_DICT

    if user_list[u_id]["global_permission_id"] == 1:
        return True

    return False

def admin_user_remove(token, u_id):
    '''
    Removes a user from slackr
    Input: (token, u_id)
    Output: {}
    '''
    print(u_id)
    if not is_user_owner(token):
        raise AccessError(description="User is not owner of slackr")
    if not is_u_id_valid(u_id):
        raise InputError(description="User id is invalid")
    if is_user_deleted(u_id):
        raise InputError(description="User has already been removed")

    requester_u_id = get_u_id(token)
    if requester_u_id == u_id:
        raise InputError(description="You can't remove yourself!")

    # Change dictionary value for user
    user_dict = init_data.USER_DICT
    user_dict[u_id]['deleted'] = True

    # Log the user out of system if they're logged in
    invalidate_user_session(u_id)

    # Remove user from channels they're part of
    remove_user_from_channels(u_id)
    print (u_id)
    print(user_dict)
    return {}

def admin_userpermissions_change(token, u_id, permission_id):
    '''
    Changes the user permisions if token input is owner of slackr
    Input: (token, u_id, permission_id)
    Output: {}
    '''
    # Checking for InputErrors
    # Check that token is valid
    if not is_token_valid(token):
        raise InputError(description="Token is invalid")
    # Check that user if entered is valid
    if not is_u_id_valid(u_id):
        raise InputError(description="User does not exist in the system")

    # Check that permission_id entered is valid
    if not is_permission_id_valid(permission_id):
        raise InputError(description="permission_id entered is invalid")
    # Checking for AccessErrors
    if not is_user_owner(token):
        raise AccessError(description="User isn't owner")

    # Change permissions for user with u_id
    init_data.USER_DICT[u_id]["global_permission_id"] = permission_id

    return {}

def channels_list(u_id):
    """
    channel_list, returns a list of all channels
    that that the user is a "member" of and the associated channel details.
    Input: token
    Output: channels
    """

    # Obtain channel dictionary from the data store
    channels = init_data.CHANNELS_DICT

    # Create empty channels dictionary return for the users channel
    user_channels = {
        "channel_id":"",
        "name":""
    }

    # Create empty list to be filled with channel dictionaries
    channel_list = []

    # Loop through channels dictionary to obtain channel_id and channel name that belongs to user
    for key in channels:
        # Create list of members in each channel
        members = channels[key]["members"]
        for idx in members:
            if idx["u_id"] == u_id:
                user_channels["channel_id"] = key
                user_channels["name"] = channels[key]["name"]
                channel_list.append({
                    "channel_id":key,
                    "name":channels[key]["name"]
                })

    return channel_list
