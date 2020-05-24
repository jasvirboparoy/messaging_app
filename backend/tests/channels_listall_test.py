from random import seed
import pytest
import init_data
from src.error import InputError, AccessError
from src.channel import channel_invite, channel_join
from src.channels import channels_create, channels_listall
from src.auth import auth_register
from src.workspace import reset_workspace

# Tests the functionality of function channels_listall

# ASSUMPTIONS
# assumes that channels_create, channel_invite, channel_join
# channel_leave, channel_removeowner works
# assume that "associated channel detail" is the channel_id
# and name

def test_list_all():
    # testing that channel_list list of all channels that user is in
    # creates list of channels created to be cross checked
    # with return value of channel_list

    reset_workspace()
    
    """# DELETE THIS
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]"""

    # user 1 registers to slackr and creates a public channel
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]

    channel1 = channels_create(token1, "channel_1", True)

    c_id1 = channel1["channel_id"]

    # user 2 registers to slackr, create a channel, joins a channel
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results2["token"]

    u_id2 = results2["u_id"]

    channel2 = channels_create(token1, "channel_2", False)

    c_id2 = channel2["channel_id"]

    channel_join(token2, c_id1)

    # user 3 register to slackr and creates channel, invites user to a channel
    results3 = auth_register("jasivir@gmail.com", "abcdEF12", "Jasivir", "Boparoy")
    token3 = results3["token"]

    channel3 = channels_create(token3, "channel_3", False)

    c_id3 = channel3["channel_id"]

    channel_invite(token3, c_id3, u_id2)

    # NEW TEST
    channel_dict = init_data.CHANNELS_DICT
    channels = channels_listall(token1)

    # Checking if all three
    result = 0
    for key in channel_dict:
        for idx in channels["channels"]:
            if channel_dict[key] == idx["channel_id"]:
                result += 1
    
    assert result == 3
    reset_workspace()

def test_list_all_not():
    # testing that channel_list list of all channels that user is in
    # creates list of channels created to be cross checked
    # with return value of channel_list

    # user 1 registers to slackr and creates a public channel
    results1 = auth_register("catpotter18@gmail.com", "abcdEF12", "Catherine", "Trinh")
    token1 = results1["token"]

    channel1 = channels_create(token1, "channel_1", True)

    c_id1 = channel1["channel_id"]

    # user 2 registers to slackr, create a channel, joins a channel
    results2 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")
    token2 = results2["token"]

    u_id2 = results2["u_id"]

    channel2 = channels_create(token1, "channel_2", False)

    c_id2 = channel2["channel_id"]

    channel_join(token2, c_id1)

    # user 3 register to slackr and creates channel, invites user to a channel
    results3 = auth_register("jasivir@gmail.com", "abcdEF12", "Jasivir", "Boparoy")
    token3 = results3["token"]

    channel3 = channels_create(token3, "channel_3", False)

    c_id3 = channel3["channel_id"]

    channel_invite(token3, c_id3, u_id2)

    # Generate random invalid c_id that does not already exist
    invalid_c_id = seed(1)
    while invalid_c_id == c_id1 and invalid_c_id == c_id2 and invalid_c_id == c_id3:
        invalid_c_id = seed(1)

    # Test that invalid channel is not in return of channel_listall
    channels = channels_listall(token3)["channels"]

    for channel in range(len(channels)):
        assert channels[channel]["channel_id"] != invalid_c_id

    reset_workspace()