''' File contains helper functions related to users '''
import init_data
from src.error import AccessError

def get_u_id(token):
    '''
    Gets the user id of a given token
    Input: token
    Output: u_id or none
    '''
    if not is_token_valid(token):
        raise AccessError(description="Invalid token")

    tokens_list = init_data.TOKENS_DICT

    return tokens_list['valid_tokens'][token]

def is_token_valid(token):
    '''
    Checks whether token is active for system
    Input: token
    Output: Boolean
    '''
    tokens_list = init_data.TOKENS_DICT
    for key in tokens_list['valid_tokens']:
        if key == token:
            return True

    return False

def is_u_id_valid(u_id):
    """
    Checks if u_id exists in the slackr server
    Input: u_id
    Output: Boolean
    """
    for user in init_data.USER_DICT.keys():
        if u_id == user:
            return True

    return False

def is_user_deleted(u_id):
    '''
    Checks whether a user is deleted
    Input: u_id
    Output: Boolean
    '''
    user_dict = init_data.USER_DICT
    if user_dict[u_id]['deleted']:
        return True
    return False
