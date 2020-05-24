import pytest
from src.error import InputError, AccessError
from src.message import message_send, message_remove, message_react
from src.channels import channels_create
from src.auth import auth_register
from src.workspace import reset_workspace
import init_data

# given correct input test message remove is working
def test_message_react_with_correct_inputs():
    reset_workspace()

    # create a user and get its u_id and token
    user_one = auth_register("123456@gmail.com", "asd!@#", "grace", "yin")

    # create a new channel
    channel_one = channels_create(user_one['token'], "channel_1", True)
    c_id_one = channel_one['channel_id']

    # create a new message
    message_id_one = message_send(user_one['token'], c_id_one, "Hello world!")

    # add a react to the message
    message_react(user_one['token'], message_id_one, "1")

    assert init_data.MESSAGES_DICT[c_id_one]["reacts"] == ["1"]

