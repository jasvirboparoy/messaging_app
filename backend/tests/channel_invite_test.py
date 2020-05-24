import pytest
from src.error import InputError, AccessError
from src.channel import channel_invite , channel_join, channel_details
from src.channels import channels_create
from src.auth import auth_register, auth_logout
from src.workspace  import reset_workspace

##
# Assume channel_create, join, and details is working 
# Assume auth_register works
# assume auth_logout works

#Assume invite function will not be performed on a public channel

#two functions to get a new user and new channel
@pytest.fixture
def get_2nd_user():
    reset_workspace()
    user = auth_register("jasvir@gmail.com","testword","Jas", "Bop")
    return(user["u_id"],user["token"])


@pytest.fixture
def get_user_and_channel():
    user = auth_register("ernest@gmail.com","testword","Ernest", "Yee")
    c_id = channels_create(user["token"],"testchannel",False)
    return (c_id["channel_id"], user["u_id"],user["token"])

def test_channel_invite(get_2nd_user,get_user_and_channel):
    u_id2, token2 = get_2nd_user

    c_id, u_id, token = get_user_and_channel #private channel is created

    #invite a second user to the channel
    channel_invite(token, c_id, u_id2)

    details = channel_details(token,c_id)

    for members in details["all_members"]:
        assert members["u_id"] in [u_id,u_id2]

    reset_workspace()

def test_channel_invite_inputerror1(get_2nd_user,get_user_and_channel):
    # input errors for invalid channel_id and for invalid user
    
    u_id2, token2 = get_2nd_user

    c_id, u_id, token = get_user_and_channel #private channel is created

    #assume c_id in the test is not a valid c_id
    with pytest.raises(InputError) as e:
        channel_invite(token, 1234567, u_id2)

    with pytest.raises(InputError) as e:
        channel_invite(token, 9382914800, u_id2)

    # 2 - assume u_id in the test is not a valid u_id

    with pytest.raises(InputError) as e:
        channel_invite(token, c_id, 1234565)

    with pytest.raises(InputError) as e:
        channel_invite(token, c_id, 90215712384)

    reset_workspace()


def test_channel_invite_accesserror(get_2nd_user,get_user_and_channel):
    # accesserror when user is already a member of channel

    u_id2, token2 = get_2nd_user

    c_id, u_id, token = get_user_and_channel #private channel is created

    # user inviting is not a member of channel
    with pytest.raises(AccessError) as e:
        channel_invite(token2, c_id, u_id)

    with pytest.raises(AccessError) as e:
        channel_invite(token2, c_id, u_id2)

    reset_workspace()