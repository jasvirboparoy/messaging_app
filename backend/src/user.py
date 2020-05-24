''' This file contains the functions for user '''
import init_data
from src.auth import is_token_valid, is_email_invalid
from src.error import InputError
from src.user_helper import get_u_id, is_u_id_valid
from src.auth import is_email_used
from src.channel_helper import get_channel_id

def is_handle_str_used(handle_str):
    '''
    Function checks whether handle_str is used
    Input:  handle_str
    Output: Boolean (True if handle_str used)
    '''
    # get user dictionary from data store
    users = init_data.USER_DICT

    # create empty list to store handle_str
    handle_str_list = []

    # Put all used handle_str into handle_str_list
    for key in users:
        handle_str_list.append(users[key]['handle_str'])

    # Check if handle_str has been used
    if handle_str in handle_str_list:
        return True

    # Return false if handle_str not used
    return False


def user_profile(token, u_id):
    '''
    input: token, u_id
    output: emial, name_first, name_last, handle_str
    '''

    #check is token valid
    if not is_token_valid(token):
        raise InputError(description="token is invalid")

    # check is u_id valid
    if not is_u_id_valid(u_id):
        raise InputError(description="User with u_id is not a valid user")

    #creat an empty dictionary to store user information
    user_data = {}

    user_data['u_id'] = u_id
    user_data['email'] = init_data.USER_DICT[u_id]['email']
    user_data['name_first'] = init_data.USER_DICT[u_id]['name_first']
    user_data['name_last'] = init_data.USER_DICT[u_id]['name_last']
    user_data['handle_str'] = init_data.USER_DICT[u_id]['handle_str']
    user_data['profile_img_url'] = init_data.USER_DICT[u_id]['profile_img_url']

    return {'user': user_data}

def user_profile_setname(token, name_first, name_last):
    '''
    input: token, name_first, name_last
    output:
    '''
    #check is token valid
    if not is_token_valid(token):
        raise InputError(description="token is invalid")

    #check is length of name_first is vaild
    if (len(name_first) > 49 or len(name_first) < 2):
        raise InputError(description="name_first is not between 1 and 50 characters")

    #check is length of name_last is vaild
    if (len(name_last) > 49 or len(name_last) < 2):
        raise InputError(description="name_last is not between 1 and 50 characters")

    u_id = get_u_id(token)
    init_data.USER_DICT[u_id]['name_first'] = name_first
    init_data.USER_DICT[u_id]['name_last'] = name_last

    # returns a list of c_id the user is part of
    c_ids = get_channel_id(u_id)
    channels = init_data.CHANNELS_DICT

    # changes the name in channels dictionary also
    for c_id in c_ids:

        for member in channels[c_id]["members"]:
            if u_id == member["u_id"]:
                member["name_first"] = name_first
                member["name_last"] = name_last

        for owner in channels[c_id]["owners"]:
            if u_id == owner["u_id"]:
                owner["name_first"] = name_first
                owner["name_last"] = name_last

    return {}

def user_profile_setemail(token, email):
    '''
    input: token, email
    output:
    '''
    #check is token valid
    if not is_token_valid(token):
        raise InputError(description="token is invalid")

    #check is the input email a valid email
    if is_email_invalid(email):
        raise InputError(description="Email entered is not a valid email")

    # check if the email is used
    if is_email_used(email):
        raise InputError(description="Email address is already being used by another user")

    u_id = get_u_id(token)
    init_data.USER_DICT[u_id]['email'] = email

    return {}

def user_profile_sethandle(token, handle_str):
    '''
    input: token, handle_str
    output:
    '''
    #check is token valid
    if not is_token_valid(token):
        raise InputError(description="token is invalid")

    #check is length of handle_str between 2 and 20 characters
    if (len(handle_str) > 19 or len(handle_str) < 3):
        raise InputError(description="handle_str must be between 2 and 20 characters inclusive")

    # check if handle_str is already used by another user
    if is_handle_str_used(handle_str):
        raise InputError(description="handle is already used by another user")

    u_id = get_u_id(token)
    init_data.USER_DICT[u_id]['handle_str'] = handle_str

    return {}
