import pytest
from src.message import message_send
from src.channels import channels_create
from src.auth import auth_register
from src.workspace import reset_workspace
import init_data

def test_hangman():
    
    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    fir_message_id = message_send(user_one['token'], c_id_one, "/hangman")
    
    assert init_data.MESSAGES_DICT[c_id_one] == ''
    '''

def test_hangman_two():
    
    
    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    fir_message_id = message_send(user_one['token'], c_id_one, "/hangman")
    
    sec_message_id = message_send(user_one['token'], c_id_one, "/guess A")
    
    assert init_data.HANGMAN[c_id_one] = ''
    
    
def test_hangman_three():

    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    fir_message_id = message_send(user_one['token'], c_id_one, "/hangman")
    
    sec_message_id = message_send(user_one['token'], c_id_one, "/guess A")
    
    thr_message_id = message_send(user_one['token'], c_id_one, "/guess A")
    
    assert init_data.HANGMAN[c_id_one] = ''



def test_hangman_four():

    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    fir_message_id = message_send(user_one['token'], c_id_one, "/hangman")
    
    sec_message_id = message_send(user_one['token'], c_id_one, "/guess A")
    
    thr_message_id = message_send(user_one['token'], c_id_one, "/guess -")
    
    assert init_data.HANGMAN[c_id_one] = ''



def test_hangman_five():

    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    fir_message_id = message_send(user_one['token'], c_id_one, "/hangman")
    
    sec_message_id = message_send(user_one['token'], c_id_one, "/guess A")
    
    thr_message_id = message_send(user_one['token'], c_id_one, "/guess aiden")
    
    assert init_data.MESSAGES_DICT[c_id_one] = ''
    
    
    
def test_hangman_six():

    reset_workspace()
    
    # create a user and get its u_id and token
    user_one = auth_register("1747960409@qq.com", "asd!@#", "aiden", "shi")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    
    c_id_one = channel_one['channel_id']
    
    fir_message_id = message_send(user_one['token'], c_id_one, "/hangman")
    
    sec_message_id = message_send(user_one['token'], c_id_one, "/guess b")
   
    
    assert init_data.HANGMAN[c_id_one] = ''

    '''
    
    
