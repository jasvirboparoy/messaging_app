''' File contains functions for messaging '''
import uuid
import time
import threading
import init_data
from src.error import InputError, AccessError
from src.channel_helper import get_channel_id
from src.channel import get_u_id, is_user_in_channel, is_channel_id_valid, user_channel_permissions
from src.hangman import hangman_start, hangman_check, check_guess
RETURN_MESSAGE_DETAIL = {}

def generate_message_id(c_id):
    '''
    Creates a new message_id
    Input:
    Output: unique message_id generated using uuid1 (integer return)
    '''
    return len(init_data.MESSAGES_DICT[c_id]) + 1

def message_send(token, channel_id, message):
    
    '''
    Sends a message in a channel
    Input: (token, channel_id, message)
    Output: { message_id }
    '''

    u_id = get_u_id(token)

    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")

    if not is_user_in_channel(u_id, channel_id):
        raise AccessError(description="You are not a member of channel")

    message_id = generate_message_id(channel_id)
    time_created = int(time.time())

    new_message = {}

    new_message["message_id"] = message_id
    new_message["u_id"] = u_id
    new_message["message"] = message
    new_message["time_created"] = time_created
    new_message["is_pinned"] = False
    new_message["react"] = ""
    
    # pull out all c_ids in message_dict
    message_dict = init_data.MESSAGES_DICT
    c_ids = [c_id for c_id in message_dict]

    # check if message_dict already contains a list of messages
    if channel_id in c_ids:
        init_data.MESSAGES_DICT[channel_id].insert(0,new_message)
    # if message is the first one in the channel_id make a new list and insert message in list 
    else:
        init_data.MESSAGES_DICT[channel_id] = []
        init_data.MESSAGES_DICT[channel_id].insert(0,new_message)

    # Hangman conditions
    if (message == '/hangman'):
        hangman_start(channel_id, token)
  
    if check_guess(message):
        hangman_check(channel_id, u_id, message)

    return {'message_id': message_id}

def get_message_sendlater_return(token, channel_id, message):
    '''
    Used to get return from message send function and
    store it in RETURN_MESSAGE_DETAIL global variable
    Input: (token, channel_id, message)
    Output:
    '''
    global RETURN_MESSAGE_DETAIL
    RETURN_MESSAGE_DETAIL = message_send(token, channel_id, message)

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Sends a message at a later time
    Input: (token, channel_id, message, time_sent)
    Output: { message_id }
    '''

    u_id = get_u_id(token)

    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel ID not valid channel")

    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")

    current_time = int(time.time())

    if (time_sent - current_time) < 0:
        raise InputError(description="Time sent is time in past")

    if not is_user_in_channel(u_id, channel_id):
        raise AccessError(description="User is not part of channel")

    time_required = float(time_sent - current_time)

    thread = threading.Timer(time_required, get_message_sendlater_return(token, channel_id, message))
    thread.start()
    thread.join()

    init_data.MESSAGES_DICT[channel_id][0]['time_created'] = current_time
    init_data.MESSAGES_DICT[channel_id][0]['time_sent'] = int(time.time())

    message_id = RETURN_MESSAGE_DETAIL['message_id']
    return {'message_id': message_id}

def message_remove(token, message_id):
    '''
    Removes a message in a channel
    Input: (token, message_id)
    Output: {}
    '''
    # get editer information
    u_id = get_u_id(token)
    count = 0
    for key in init_data.MESSAGES_DICT:
        i = 0
        while i < len(init_data.MESSAGES_DICT[key]):
        
            if init_data.MESSAGES_DICT[key][i]['message_id'] == message_id:
                channel_id = key
                count += 1
            i += 1
    if count == 0:
        raise InputError(description= "Message (based on ID) no longer exists")
            
    count = 0
    i = 0
    while i < len(init_data.MESSAGES_DICT[channel_id]):
        
        if init_data.MESSAGES_DICT[channel_id][i]['message_id'] == message_id:
            count = i
            
        i += 1
    permission = user_channel_permissions(u_id, channel_id)
    # if the editer is not the authorised user, invalid
    # if the editer is not in the channel
    # if the editer is not an owner
    if init_data.MESSAGES_DICT[channel_id][count]['u_id'] != u_id:
        raise AccessError(description = "Unauthorised user")
    if not is_user_in_channel(u_id, channel_id):
        raise AccessError(description = "Unauthorised user")
    if permission == 1:
        raise AccessError(description = "Unauthorised user")

    del init_data.MESSAGES_DICT[channel_id][count]

    return {}


def message_edit(token, message_id, message):
    '''
    output is {}
    AccessError when none of the following are true:
    Message with message_id was sent by the authorised user making this request
    The authorised user is an owner of this channel or the slackr
    '''
    # get editer information
    u_id = get_u_id(token)
    
    for key in init_data.MESSAGES_DICT:
        i = 0
        while i < len(init_data.MESSAGES_DICT[key]):
        
            if init_data.MESSAGES_DICT[key][i]['message_id'] == message_id:
                channel_id = key
            i += 1
    count = 0
    i = 0
    while i < len(init_data.MESSAGES_DICT[channel_id]):
        
        if init_data.MESSAGES_DICT[channel_id][i]['message_id'] == message_id:
            count = i
            
        i += 1
    
    permission = user_channel_permissions(u_id, channel_id)
    # if the editer is not the authorised user, invalid
    # if the editer is not in the channel
    # if the editer is not an owner
    if init_data.MESSAGES_DICT[channel_id][count]['u_id'] != u_id:
        raise AccessError(description = "Unauthorised user")
    if not is_user_in_channel(u_id, channel_id):
        raise AccessError(description = "Unauthorised user")
    if permission == 1:
        raise AccessError(description = "Unauthorised user")
 
   
    if message == "":
        message_remove(token, message_id)
        return {}
    
    i = 0
    while i < len(init_data.MESSAGES_DICT[channel_id]):
        
        if init_data.MESSAGES_DICT[channel_id][i]['message_id'] == message_id:
            init_data.MESSAGES_DICT[channel_id][i]['message'] = message
        i += 1

    return {}

def message_react(token, message_id, react_id):
    '''
    output is {}
    '''
    # get user's channels
    u_id = get_u_id(token)
    # channel_id = get_channel_id(u_id)

    # put all the messages in this channel into a list
    messages_in_this_channel = []

    i = 0
    for key in init_data.MESSAGES_DICT:
        while i < len(init_data.MESSAGES_DICT[key]):
            channel_id = key
            messages_in_this_channel.append(init_data.MESSAGES_DICT[channel_id][i]["message_id"])
        i = i + 1

    # authorised user is not in the channel
    if message_id not in messages_in_this_channel:
        raise InputError(description = "Authorised user is invalid in this channel")

    # invalid react id
    # in Iteration 2, the only valid react ID the frontend has is 1
    if react_id != 1:
        raise InputError(description = "Invalid react_id")

    msg_dict = create_react(init_data.MESSAGES_DICT, u_id, react_id)
    
    return {}

def message_unreact(token, message_id, react_id):
    '''
    output is {}
    '''
    # get user's channels
    u_id = get_u_id(token)
    channel_id = get_channel_id(u_id)
    messages_in_this_channel = MESSAGES_DICT["channel_id"]["message_id"]

    # authorised user is not in the channel
    if message_id not in messages_in_this_channel:
        raise InputError(description = "Authorised user is invalid in this channel")
    
    # invalid react id
    # in Iteration 2, the only valid react ID the frontend has is 1
    if react_id != 1:
        raise InputError(description = "Invalid react_id")
    
    react_list = MESSAGES_DICT["reacts"]
    is_react_exist = define_react(react_list, react_id)
    if is_react_exist == -1:
        raise InputError(description = "React does not exist")
    react_list.remove("u_id")

def message_pin(token, message_id):
    '''
    output is {}
    '''
    # get user information
    u_id = get_u_id(token)
    channel_id = get_channel_id(u_id)
    messages_in_this_channel = MESSAGES_DICT["channel_id"]["message_id"]

    # invalid message
    message = read_message(message_id)
    if len(message)>1000 or len(message)<1:
        raise InputError(description = "The message is invalid, please check message length (between 1 and 1000 characters)")

    # authorised user is not an owner
    permission_id = user_channel_permissions(u_id, channel_id)
    if permission_id != 1:
        raise InputError(description = "Invalid permission, not an owner")

    # message already pined
    if message["is_pinned"] == True:
        raise InputError(description = "Message already pinned")

    # authorised user is not in the channel
    if message_id not in messages_in_this_channel:
        raise InputError(description = "Authorised user is invalid in this channel")

    message["is_pinned"] == True

def message_unpin(token, message_id):
    '''
    output is {}
    '''
    # get user information
    u_id = get_u_id(token)
    channel_id = get_channel_id(u_id)
    messages_in_this_channel = MESSAGES_DICT["channel_id"]["message_id"]

    # invalid message
    message = read_message(message_id)
    if len(message)>1000 or len(message)<1:
        raise InputError(description = "The message is invalid, please check message length (between 1 and 1000 characters)")

    # authorised user is not an owner
    permission_id = user_channel_permissions(u_id, channel_id)
    if permission_id != 1:
        raise InputError(description = "Invalid permission, not an owner")

    # message already unpinned
    if message["is_pinned"] == False:
        raise InputError(description = "Message already unpinned")

    # authorised user is not in the channel
    if message_id not in messages_in_this_channel:
        raise InputError(description = "Authorised user is invalid in this channel")

    message["is_pinned"] == False

# help functions

def read_message(channel_id, message_id):
    i = 0
    while i < len(MESSAGES_DICT["channel_id"]):
        if MESSAGES_DICT["c_id"][i]["message_id"] == message_id:
            message = (MESSAGES_DICT["c_id"][i]["message"])
        i = i + 1
    return message

def create_react(MESSAGES_DICT, u_id, react_id):
    REACT_DICT = {
        "react_id":"",
        "u_ids":"",
    }
    react_list = MESSAGES_DICT["reacts"]
    is_react_exist = define_react(react_list, react_id)
    if is_react_exist == -1:
        REACT_DICT["react_id"] = react_id
        REACT_DICT["u_ids"].append(u_id)
        MESSAGES_DICT["reacts"].append(REACT_DICT)
    else:
        react_dict = react_list[is_react_exist]
        if u_id in react_dict['u_ids']:
            raise InputError(description="Existing react")
        react_dict['u_ids'].append(u_id)
    return MESSAGES_DICT

def define_react(react_list, react_id):
    i = 0
    for react in react_list:
        if react["react_id"] == react_id:
            return i
        i = i + 1
    return -1

def define_react(react_list, react_id):
    i = 0
    for react in react_list:
        if react["react_id"] == react_id:
            return i
        i = i + 1
    return -1

