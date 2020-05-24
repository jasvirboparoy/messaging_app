''' This file contains the users all function '''
from src.error import InputError
from src.user_helper import is_token_valid, is_user_deleted
import init_data

def users_all(token):
    '''
    Input: token
    Output: List of dictionaries, where each dictionary contains types u_id, 
    email, name_first, name_last, handle_str
    '''
    #check is token valid
    if not is_token_valid(token):
        raise InputError(description="token is invalid")

    users_list = []
    for key in init_data.USER_DICT:
        u_id = key

        if not is_user_deleted(u_id):
            user_data = {}

            user_data['u_id'] = u_id
            user_data['email'] = init_data.USER_DICT[u_id]['email']
            user_data['name_first'] = init_data.USER_DICT[u_id]['name_first']
            user_data['name_last'] = init_data.USER_DICT[u_id]['name_last']
            user_data['handle_str'] = init_data.USER_DICT[u_id]['handle_str']
            user_data['profile_img_url'] = init_data.USER_DICT[u_id]['profile_img_url']
            users_list.append(user_data)

    users_dic = {
        'users' : users_list
    }

    return users_dic
