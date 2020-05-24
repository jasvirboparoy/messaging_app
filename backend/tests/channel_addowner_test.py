import pytest
from src.error import InputError, AccessError
from src.channel import channel_invite , channel_join, channel_details, channel_addowner
from src.channels import channels_create
from src.auth import auth_register, auth_logout
from src.workspace import reset_workspace

##
# Assume channel_create, invite, and details is working 
# Assume auth_register works
# assume auth_logout works

#Assume invite function will not be performed on a public channel

#two functions to get a new user and new channel
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

# Function will setup a private channel with 5 users and user 1 as an owner
# Returns a list of all users, and a channel_id
@pytest.fixture
def setup_channel(get_5_new_users):

    # assign variable to list of 5 users created from auth register
    users_all = get_5_new_users

    # Assign each element in users_all list to user
    user_1 = users_all[0]
    user_2 = users_all[1]
    user_3 = users_all[2]
    user_4 = users_all[3]
    user_5 = users_all[4]

    # Create a private channel called tester using user_1 token
    # Therefore user[0] in tests below will be the orginal owner for all tests
    test_channel = channels_create(user_1['token'], "Tester", False)

    # Add user_2,3,4,5 to private channel
    channel_invite(user_1['token'], test_channel['channel_id'], user_2['u_id'])
    channel_invite(user_1['token'], test_channel['channel_id'], user_3['u_id'])
    channel_invite(user_1['token'], test_channel['channel_id'], user_4['u_id'])
    channel_invite(user_1['token'], test_channel['channel_id'], user_5['u_id'])

    return (users_all, test_channel["channel_id"])
def test_channel_addowner_basic(setup_channel):
    # Tests for basic functionality by adding 1 users from original user persepective

    user, c_id = setup_channel

    channel_addowner(user[0]["token"], c_id, user[1]["u_id"])

    # Assert that both user 1 and user 2 are owners in the same channel
    owner_members = channel_details(user[0]["token"], c_id)["owner_members"]
    owner_members_u_ids = [member['u_id'] for member in owner_members]
    assert user[1]["u_id"] in owner_members_u_ids
    assert user[0]["u_id"] in owner_members_u_ids
    
    reset_workspace()

def test_channel_addowner_multiple(setup_channel):
    # Tests for basic functionality by adding multiple users from original user persepective

    user, c_id = setup_channel

    channel_addowner(user[0]["token"], c_id, user[1]["u_id"])
    channel_addowner(user[0]["token"], c_id, user[2]["u_id"])
    channel_addowner(user[0]["token"], c_id, user[3]["u_id"])

    # Assert that added owners are owners in the same channel
    owner_members = channel_details(user[0]["token"], c_id)["owner_members"]
    owner_members_u_ids = [member['u_id'] for member in owner_members]
    
    assert user[3]["u_id"] in owner_members_u_ids
    assert user[2]["u_id"] in owner_members_u_ids
    assert user[1]["u_id"] in owner_members_u_ids
    assert user[0]["u_id"] in owner_members_u_ids

    reset_workspace()

def test_channel_addowner_inputerror(setup_channel):
    #tests for inputerrors

    user, c_id = setup_channel

    # Assume that -111111 and -111113 is not a valid channel id
    with pytest.raises(InputError) as e:
        channel_addowner(user[0]["token"], -111111, user[1]["u_id"])
    
    with pytest.raises(InputError) as e:
        channel_addowner(user[0]["token"], -111113, user[1]["u_id"])

    # Add 2 users as an owner already and tries to add them in again
    channel_addowner(user[0]["token"], c_id, user[1]["u_id"])
    channel_addowner(user[0]["token"], c_id, user[2]["u_id"])

    with pytest.raises(InputError) as e:
        channel_addowner(user[0]["token"], c_id, user[1]["u_id"])
    with pytest.raises(InputError) as e:
        channel_addowner(user[0]["token"], c_id, user[2]["u_id"])
    
    reset_workspace()

def test_channel_addowner_accesserror(setup_channel):
    #tests for accesserrors

    user, c_id = setup_channel

    # Accesserror when user[1] tries to add themself or another user as an owner
    with pytest.raises(AccessError) as e:
        channel_addowner(user[1]["token"], c_id, user[2]["u_id"])
    
    with pytest.raises(AccessError) as e:
        channel_addowner(user[1]["token"], c_id, user[1]["u_id"])
    """
    # Add 2 users as an owner already and tries to add them in again
    channel_addowner(user[0]["token"], c_id, user[1]["u_id"])
    channel_addowner(user[0]["token"], c_id, user[2]["u_id"])

    with pytest.raises(AccessError) as e:
        channel_addowner(user[0]["token"], c_id, user[1]["u_id"])
    with pytest.raises(AccessError) as e:
        channel_addowner(user[0]["token"], c_id, user[2]["u_id"])
    """
    reset_workspace()