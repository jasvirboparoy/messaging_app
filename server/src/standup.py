from src.error import InputError, AccessError
import init_data
from src.channels import channels_create
from src.message import message_sendlater
from src.error import InputError, AccessError
from datetime import datetime, timezone, timedelta
from src.channel import get_u_id, is_token_valid, is_user_in_channel, is_channel_id_valid
# from datetime import timedelta
import threading
import time

# Checks message is valid
def is_message_valid(message):
    if len(message) <= 1000:
        return True

    return False

def is_active_standup(channel_id):
    '''
    Checks if active standup started
    Assumes channel_id is valid
    Input: channel_id
    Output: Boolean
    '''
    channel = init_data.CHANNELS_DICT[channel_id]
    for key in channel:
        if key == 'standup':
            return channel[key]['is_active']
    return False

# This function starts and defines the standup period
def standup_start(token, channel_id, length):
    '''
    Starts a standup for channel
    Input: (token, channel_id, length)
    Output: { time_finish }
    '''
    # Get user id
    u_id = get_u_id(token)

    # Checking channel is all valid
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel does not exist in slackr")
    if not is_user_in_channel(channel_id, u_id):
        raise InputError(description="User is not a member of the channel")

    # Check that a standup does not already exist in the channel
    standup = standup_active(token, channel_id)
    if standup['is_active']:
        raise InputError(description="There's already an active standup")

    # Check that length entered is valid
    if length < 0:
        raise InputError(description="Time length entered is invalid")

    # Calculate time_finish
    time_finish = int(datetime.timestamp(datetime.now() + timedelta(seconds=length)))

    # Update data in system to say standup active now
    channel = init_data.CHANNELS_DICT[channel_id]
    channel['standup'] = {
        'is_active': True,
        'time_finish': time_finish,
        'token_started': token
        }

    # message_sendlater(token, channel_id, message, time_finish)
    return {'time_finish': time_finish}

def standup_active(token, channel_id):
    '''
    Checks whether standup is active in channel
    Input: (token, channel_id)
    Output: { is_active, time_finish }
    '''
    # Get user id
    u_id = get_u_id(token)

    # Checking channel is valid
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel does not exist in slackr")
    if not is_user_in_channel(channel_id, u_id):
        raise InputError(description="User is not a member of the channel")

    # Creat empty return dictionary
    standup_details = {}

    # Checking if a standup exists in the channel
    if is_active_standup(channel_id):
        standup_details['is_active'] = True
        time_finish = init_data.CHANNELS_DICT[channel_id]['standup']['time_finish'] 
        standup_details['time_finish'] = time_finish
        return standup_details

    standup_details['is_active'] = False
    standup_details['time_finish'] = None
    return standup_details

def standup_send(token, channel_id, message):
    '''
    Sends a message to get buffered in standup queue
    assuming standup is active
    Input: (token, channel_id, message)
    Output: {}
    '''
    # Get user id
    u_id = get_u_id(token)

    # Checking channel is valid
    if not is_channel_id_valid(channel_id):
        raise InputError(description="Channel does not exist in slackr")
    if not is_user_in_channel(channel_id, u_id):
        raise InputError(description="User is not a member of the channel")

    # Checking if the message is invalid
    if len(message) > 1000:
        raise InputError(description="Message is too long")

    standup_details = standup_active(token, channel_id)
    if not standup_details['is_active']:
        raise InputError(description="No active standup")
    
    time_finish = init_data.CHANNELS_DICT[channel_id]['standup']

    # Check that timestamp for function call is valid
    # Standup_send is not called past time_finish
    if int(datetime.timestamp(datetime.now())) > time_finish:
        raise InputError(description="The standup period has closed")

    # Creating empty message string from user
    # Obtain user name
    members = init_data.CHANNELS_DICT[channel_id]["members"]

    # Loop through list of members to obtain users first name
    for key in members:
        if members[key]["u_id"] == u_id:
            first_name = members[key]["first_name"]

    user_message = first_name + ": " + message + "\n"

    # Add message to buffer string in data system
    # standup_message = init_data.STANDUP_DICT[channel_id]["message_buffer"].insert(user_message)

    # Add message to buffer
    message_buffer = init_data.CHANNELS_DICT[channel_id]['standup']['message_buffer']
    message_buffer = message_buffer + user_message

    return {}
