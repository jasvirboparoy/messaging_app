'''
This file contains helper functions for channel
functions
'''

import init_data

def get_channel_id(u_id):
    """
    Given a certain u_id returns a list of channel_id's that a user is part of.
    Input: u_id
    Output: List of channel_ids
    """
    user_channels = []
    channels = init_data.CHANNELS_DICT
    for channel in channels:
        for members in channels[channel]["members"]:
            if members["u_id"] == u_id:
                user_channels.append(channel)

    return user_channels

def is_channel_id_valid(channel_id):
    '''
    Checks whether channel_id has been created
    Input: channel_id
    Output: Boolean
    '''
    for c_id in init_data.CHANNELS_DICT:
        if c_id == int(channel_id):
            return True

    return False

def is_user_in_channel(u_id, c_id):
    """
    Check user is in channel
    Input: u_id,c_id
    Output:Boolean
    """

    channel_members = init_data.CHANNELS_DICT[c_id]["members"]
    for members in channel_members:
        if u_id == members["u_id"]:
            return True
    return False

def user_channel_permissions(u_id, channel_id):
    '''
    Gets the permission type of a user for a channel
    Input: u_id, channel_id
    Output: {permission_id}
    -1 if user not in channel
    '''
    channel_info = init_data.CHANNELS_DICT[channel_id]

    owners = channel_info['owners']
    members = channel_info['members']

    for user in owners:
        if user['u_id'] == u_id:
            return {'permission_id': 1}

    for user in members:
        if user['u_id'] == u_id:
            return {'permission_id': 2}

    return {'permission_id': -1}
