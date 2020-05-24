import pytest
from src.error import InputError, AccessError
from src.message import message_send, message_remove
from src.channels import channels_create
from src.auth import auth_register
from src.workspace import reset_workspace
import init_data


# This file contains tests for message_remove function
# given (token, message_id), return {}

# Define the user information

# given correct input test message remove is working
def test_message_remove_with_correct_inputs():
    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    # send messages to the channel
    fir_message_id = message_send(user_one['token'], c_id_one, "Hi guys, i am wabalaba")

    message_remove(user_one['token'], fir_message_id['message_id'])
    
    assert init_data.MESSAGES_DICT[c_id_one] == []
