import pytest
from src.channels import channels_create
from src.channel import channel_join, channel_details
from src.error import InputError, AccessError
from src.auth import auth_register
from src.workspace import reset_workspace

## channel_join test functions 
# Assume channel_detail works 
# Assume channels_create works
# Assume auth_register works

# Test - norm:
# create a new user and assert channel_details is the same 


# Assume channel_join is not applied for private channels, as private channels will 
# not be visible
@pytest.fixture
def get_5_new_users():
    reset_workspace()
    user_1 = auth_register("johnsmith@gmail.com", "123456Jasvir", "John", "Smith")
    user_2 = auth_register("ohnsmith@gmail.com", "5553322545Jb", "Henry", "Smith")
    user_3 = auth_register("hnsmith@gmail.com", "111245332Jb", "Jim", "Henry")
    user_4 = auth_register("henryjohn@gmail.com", "12454334kkS", "Henry", "Ford")
    user_5 = auth_register("smith@gmail.com", "3534654654kK", "James", "Townsend")

    user_list = [user_1, user_2, user_3, user_4, user_5]
    return user_list

def test_channel_join_norm (get_5_new_users):
    user_list = get_5_new_users
    
    token1 = user_list[0]["token"]
    u_id1 = user_list[0]["u_id"]
    c_id = channels_create(token1, "testchannel", True)

    token2 = user_list[1]["token"]
    u_id2 = user_list[1]["u_id"]

    channel_join(token2, c_id["channel_id"])
    reset_workspace()
    # tests if function doesnt crash
    # will implement more comprehesive tests including channel_detail function

def test_channel_join_inputerror(get_5_new_users):
    user_list = get_5_new_users
    #tokens = [for i["token"] in user_list]

    tokens = []
    u_id = []

    for i in user_list:
        tokens.append(i["token"])
        u_id.append(i["u_id"])

    c_id = channels_create(tokens[0], "testchannel", True)

    #assume -1111 is an invalid channel_id
    with pytest.raises(InputError) as e:
        channel_join(tokens[1],-1111)

    with pytest.raises(InputError) as e:
        channel_join(tokens[2],-1111)

    with pytest.raises(InputError) as e:
        channel_join(tokens[3],-1111)
    
    with pytest.raises(InputError) as e:
        channel_join(tokens[4],-1111)

    reset_workspace()
# create a private channel wherein user is not an admin
def test_channel_join_accesserror(get_5_new_users):

    user_list = get_5_new_users

    tokens = []
    u_id = []
    for i in user_list:
        tokens.append(i["token"])
        u_id.append(i["u_id"])
    c_id = channels_create(tokens[0], "testchannel", False)

    # try joining a private channel
    with pytest.raises(AccessError) as e:
        channel_join(tokens[1],c_id["channel_id"])

    with pytest.raises(AccessError) as e:
        channel_join(tokens[2],c_id["channel_id"])

    with pytest.raises(AccessError) as e:
        channel_join(tokens[3],c_id["channel_id"])
    
    with pytest.raises(AccessError) as e:
        channel_join(tokens[4],c_id["channel_id"])

    reset_workspace()
def test_channel_join_norm2 (get_5_new_users):
    # tests here require channel_detail to work from here on out, (however channel_detail
    # requires channel_join to work so there is a dependecy between the two of these functions

    user_list = get_5_new_users
    
    token1 = user_list[0]["token"]
    u_id1 = user_list[0]["u_id"]
    c_id = channels_create(token1, "testchannel", True)

    token2 = user_list[1]["token"]
    u_id2 = user_list[1]["u_id"]

    channel_join(token2,c_id["channel_id"])

    c_details = channel_details(token1, c_id["channel_id"])

    all_members= c_details["all_members"]

    u_ids = [f["u_id"] for f in all_members]

    assert u_id1 in u_ids
    assert u_id2 in u_ids

    reset_workspace()
def test_channel_join_5_users(get_5_new_users):

    user_list = get_5_new_users

    tokens = []
    u_id = []

    for i in user_list:
        tokens.append(i["token"])
        u_id.append(i["u_id"])
    c_id = channels_create(tokens[0], "testchannel", True)

    channel_join(tokens[1], c_id["channel_id"])
    channel_join(tokens[2], c_id["channel_id"])
    channel_join(tokens[3], c_id["channel_id"])
    channel_join(tokens[4], c_id["channel_id"])

    c_details = channel_details(tokens[0], c_id["channel_id"])

    all_members= c_details["all_members"]

    all_u_ids = [f["u_id"] for f in all_members]

    assert u_id[0] in all_u_ids
    assert u_id[1] in all_u_ids
    assert u_id[2] in all_u_ids
    assert u_id[3] in all_u_ids
    assert u_id[4] in all_u_ids

    reset_workspace()