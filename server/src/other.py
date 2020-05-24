''' File contains functions for searching messages '''
import init_data
from error import InputError
from auth import is_token_valid
from channel import is_user_in_channel
from user_helper import get_u_id

def search(token, query_str):
    '''
    input: token, query_str
    output: collection of messages in all of the channels that the user
    has joined that match the query. Results are sorted from most
    recent message to least recent message
    '''
    #check is token valid
    if not is_token_valid(token):
        raise InputError(description="token is invalid")

    time_list = []
    result_message = {}
    u_id = get_u_id(token)
    j = 0

    num_ch = 0
    for c_id in init_data.CHANNELS_DICT:
        if is_user_in_channel(u_id, c_id):
            message = init_data.MESSAGES_DICT[c_id]
            i = 0

            while i < len(message):
                num_ch += 1
                if check_if_match(query_str, message[i]['message']):

                    result_message[j] = {}
                    result_message[j]['time_created'] = message[i]['time_created']
                    result_message[j]['message'] = message[i]['message']
                    time_list.append(message[i]['time_created'])
                i += 1
                j += 1

    time_list = sorted(time_list)

    message_list = []

    for item in time_list:
        for key in result_message:
            if result_message[key]['time_created'] == item:
                message_list.append(result_message[key]['message'])
                result_message[key]['time_created'] = ''
                break
    messages = {
        'messages' : message_list
    }
    return messages

def check_if_match(query_str, message):
    '''
    Checks if query matches a string
    '''
    if query_str in message:
        return True
    return False
