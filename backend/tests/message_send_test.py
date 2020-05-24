import pytest
from src.error import InputError, AccessError
from src.auth import auth_register
from src.message import message_send
from src.channels import channels_create
from src.channel import channel_join
from src.workspace import reset_workspace

# This file tests the message_send function
# given (token, channel_id, message), return { message_id }
# message_send tests

# Assume that auth_register, channels_create and channel_join work

# Define the user information
@pytest.fixture
def get_user_and_public_channel():
    reset_workspace()
    user_data = auth_register("grace.yin@gmail.com", "hello123", "Grace", "Yin")
    channel_data = channels_create(user_data['token'], "new_channel", True)
    data = [user_data, channel_data]
    return data

# Message is more than 1000 characters
def test_message_send_invalid_message(get_user_and_public_channel):
    user = get_user_and_public_channel[0]
    channel = get_user_and_public_channel[1]
    invalid_string_1 = "d" * 1001

    with pytest.raises(InputError) as e:
        message_send(user['token'], channel['channel_id'], invalid_string_1)

    invalid_string_2 = "e" * 2000

    with pytest.raises(InputError) as e:
        message_send(user['token'], channel['channel_id'], invalid_string_2)
    reset_workspace()

# the authorised user has not joined the channel they are trying to post to
def test_message_send_not_member_public(get_user_and_public_channel):

    public_channel = get_user_and_public_channel[1]

    user_2 = auth_register("johnsmith@gmail.com", "34233453453JssfB", "John", "Smith")

    with pytest.raises(AccessError) as e:
        message_send(user_2['token'], public_channel['channel_id'], "Hey!")
    reset_workspace()

# the authorised user hasn't been invited to private channel they are 
# trying to post to
def test_message_send_not_member_priv():

    # Register 2 new users
    user_1 = auth_register("grace.yin@gmail.com", "hello123", "Grace", "Yin")
    user_2 = auth_register("johnsmith@gmail.com", "34233453453JssfB", "John", "Smith")

    # Create a private channel using user_1 token
    private_channel = channels_create(user_1['token'], "private", False)

    # User_2 is not part of private channel and when they try to send a message,
    # it raises an access error
    with pytest.raises(AccessError) as e:
        message_send(user_2['token'], private_channel['channel_id'], "Helllloooooo!!")

    reset_workspace()

# test for valid message and channel_id
def test_message_send_valid():
    
    # Assign user_1 and public_channel from fixture
    user_1 = auth_register("grace.yin@gmail.com", "hello123", "Grace", "Yin")
    channel_id = channels_create(user_1['token'], "tester", True)

    # Create a second user and join public channel
    user_2 = auth_register("johnsmith@gmail.com", "34233453453JssfB", "John", "Smith")
    channel_join(user_2['token'], channel_id["channel_id"])

    # This function call should not throw an error
    message_send(user_1['token'], channel_id["channel_id"], "Heyo!")
    message_send(user_2['token'], channel_id["channel_id"], "Hey :)")

    reset_workspace()