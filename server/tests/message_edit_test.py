import pytest
from src.error import InputError, AccessError
from src.message import message_send, message_edit
from src.channels import channels_list, channels_create
from src.channel import channel_messages
from src.auth import auth_register
from src.workspace import reset_workspace
import init_data
# This file tests the message_edit function file

# This function has the following properties:
# INPUT: (token, message_id, message)
# OUTPUT: {} - empty dictionary

# Creates a list of users (each being a dictionary)

# test message edit is working with correct inputs
def test_message_edit_is_working():
    
    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    # send messages to the channel
    fir_message_id = message_send(user_one['token'], c_id_one, "Hi guys, i am wabalaba")

    message_edit(user_one['token'], fir_message_id['message_id'], "Hi guys, i am aiden not wabalaba")
    
    fir_message = given_c_id_and_m_id_find_message(c_id_one, fir_message_id['message_id'])
    assert fir_message == "Hi guys, i am aiden not wabalaba"
    
    message_edit(user_one['token'], fir_message_id['message_id'], "")
    assert init_data.MESSAGES_DICT[c_id_one] == []


def given_c_id_and_m_id_find_message(c_id, m_id):
    message = ""
    i = 0
    while i < len(init_data.MESSAGES_DICT[c_id]):
        if init_data.MESSAGES_DICT[c_id][i]['message_id'] == m_id:
            return init_data.MESSAGES_DICT[c_id][i]['message']
    return message
    
    

