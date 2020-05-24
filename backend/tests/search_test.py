import pytest
from src.error import InputError, AccessError
from src.message import message_send
from src.channels import channels_list, channels_create
from src.channel import channel_messages, channel_invite
from src.auth import auth_register
from src.other import search
from src.workspace import reset_workspace
# Assume channel_list, channels_create both work
# Assume auth_register works

'''search tests'''
'''given (token, query_str), return {messages}'''

def test_search_function():

    reset_workspace()

    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create another user and get its u_id and token
    user_two = auth_register("z5255218@unsw.edu.au", "asd123", "haochen", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    # invite user_two into the channel
    channel_invite(user_one['token'], c_id_one, user_two['u_id'])

    # send messages to the channel
    one_fir_message_id = message_send(user_one['token'], c_id_one, "Hi guy")

    one_sec_message_id = message_send(user_one['token'], c_id_one, "am i the only one here? haliluya")


    # create a new channel
    channel_two = channels_create(user_one['token'], "channel_2", False)

    c_id_two =channel_two['channel_id']

    two_fir_message_id = message_send(user_one['token'], c_id_two, "This is my own channel!!")
    
    two_sec_message_id = message_send(user_one['token'], c_id_two, "yooohooo, i am the owner!")

    one_third_message_id = message_send(user_two['token'], c_id_one, "No! u are not the only one here, i am haochen, haliluya")

    assert search(user_one['token'], "am") == {
        'messages' : [
            "No! u are not the only one here, i am haochen, haliluya",
            "am i the only one here? haliluya",
            "yooohooo, i am the owner!",
        ]
    }
    
