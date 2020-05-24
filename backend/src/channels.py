''' This file contains functions for channels '''
import init_data
from src.channel import get_u_id
from src.error import InputError, AccessError

def is_token_valid(token):
    '''
    Checks whether token is active for system
    Input: token
    Output: Boolean
    '''
    tokens_list = init_data.TOKENS_DICT
    for key in tokens_list['valid_tokens']:
        if key == token:
            return True

    return False

def generate_new_c_id():
    '''
    Creates a new c_id
    Input:
    Output: unique c_id generated using uuid1 (integer return)
    '''
    return len(init_data.CHANNELS_DICT) + 2 #uuid.uuid1(node=None, clock_seq=None).int


def channels_create(token,name,is_public ):
    """
    channel_create, creates a channel with the given "name", and with either a public
    or private property, the user corresponding to token is also made an owner of the
    channel.
    Input: token, name, is_public
    Output: channel_id
    """

    # check that the length of the name is less then 20 
    if len(name) > 20:
        raise InputError(description="Channel name is more then 20 characters ")

    # check that channel name is not already in use
    channels = init_data.CHANNELS_DICT

    for channel in channels.values():
        if name == channel["name"]: 
            raise InputError(description="Channel name is already in use")

    # Find u_id associated with active token
    if not is_token_valid(token):
        raise AccessError(description="Invalid token")
    u_id = init_data.TOKENS_DICT["valid_tokens"][token]

    # Generate a c_id
    new_c_id = generate_new_c_id()
    name_first = init_data.USER_DICT[u_id]["name_first"]
    name_last = init_data.USER_DICT[u_id]["name_last"]
    profile_img_url = init_data.USER_DICT[u_id]["profile_img_url"]

    # Store u_id as owners, members, and is_public in is_public
    init_data.CHANNELS_DICT[new_c_id] = {
        "name":name,
        "owners":[{"u_id":u_id,
                   "name_first":name_first,
                   "name_last":name_last,
                   "profile_img_url":profile_img_url
                   }],
        "members":[{"u_id":u_id,
                    "name_first":name_first,
                    "name_last":name_last,
                    "profile_img_url":profile_img_url}],
        "is_public": is_public
    }

    print (init_data.CHANNELS_DICT)

    # Initialise the message dict to store messages
    init_data.MESSAGES_DICT[new_c_id] = []

    return {"channel_id": new_c_id}

def channels_listall(token):
    """
    channel_listall, returns a list of all channels 
    that that exist on slackr and the channel details associated with each channel. 
    Input: token
    Output: channels
    """
    if not is_token_valid(token):
        raise AccessError(description="Invalid token")
    # Obtain channel dictionary from the data store
    channels_dict = init_data.CHANNELS_DICT

    # Create empty channels dictionary return for the users channel

    # Create empty list to be filled with channel dictionaries
    channel_listall = []

    # Loop through channels dictionary to obtain channel_id and channel name
    for c_id in channels_dict:
        channel_listall.append({
            "channel_id":c_id,
            "name":channels_dict[c_id]["name"]
            })

    return {"channels":channel_listall}


def channels_list(token):
    """
    channel_list, returns a list of all channels 
    that that the user is a "member" of and the associated channel details. 
    Input: token
    Output: channels
    """

    # Get user ID
    u_id = get_u_id(token)

    # Obtain channel dictionary from the data store
    channels = init_data.CHANNELS_DICT

    # Create empty channels dictionary return for the users channel 
    user_channels = {
        "channel_id":"",
        "name":""
    }

    # Create empty list to be filled with channel dictionaries
    channel_list = []

    # Loop through channels dictionary to obtain channel_id and channel name that belongs to user
    for key in channels:
        # Create list of members in each channel
        members = channels[key]["members"]
        for idx in members:
            if idx["u_id"] == u_id:
                user_channels["channel_id"] = key
                user_channels["name"] = channels[key]["name"]
                channel_list.append({
                    "channel_id":key,
                    "name":channels[key]["name"]
                })

    return {"channels":channel_list}
