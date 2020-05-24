import pytest
import init_data
from src.admin import admin_userpermissions_change
from src.error import InputError, AccessError
from src.auth import auth_register
from src.workspace import reset_workspace


##
# Assume channel_create, join, and details is working
# Assume auth_register works
# assume auth_logout works

#Assume invite function will not be performed on a public channel

#two functions to get a new user and new channel
@pytest.fixture
def get_user():
    user = auth_register("jasvir@gmail.com", "testword", "Jas", "Bop")
    return(user["u_id"], user["token"])

@pytest.fixture
def get_user2():
    user = auth_register("catherine@gmail.com", "6characters", "Catheirne", "Trinh")
    return(user["u_id"], user["token"])

@pytest.fixture
def get_permission_id():
    permission_id1 = 1
    permission_id2 = 2
    permission_id_invalid1 = 3
    permission_id_invalid12 = -1
    return [permission_id1, permission_id2, permission_id_invalid1, permission_id_invalid12]

def test_invalid_user_id(get_permission_id):
    # Assume -1111 is an invalid user_id
    invalid_user_id = -1111
    # Assign random token since token will not be generated bu auth_login
    invalid_token = "JNKOJ-/a..0 F"

    # Obtain valid permission ids
    permission_id = get_permission_id

    # Check function throw InputErrors with invlaid user_id
    with pytest.raises(InputError) as e:
        admin_userpermissions_change(invalid_token, invalid_user_id, permission_id[1])
    with pytest.raises(InputError) as e:
        admin_userpermissions_change(invalid_token, invalid_user_id, permission_id[0])

    reset_workspace()

def test_invalid_permissions_id(get_user, get_permission_id):
    # Global permissions can either be
    #   1. Owner where permission_id = 1
    #   2. Member where permission_id = 2
    reset_workspace()

    # Create user
    user = auth_register("jasvir@gmail.com", "testword", "Jas", "Bop")
    u_id = user["u_id"]
    token = user["token"]
    # return(user["u_id"], user["token"])

    # Invalid permission ids
    permission_id_invalid1 = 3
    permission_id_invalid2 = 32143
    # u_id, token = get_user
    # permission_id = get_permission_id

    # Check function throw InputErrors with invlaid permission_id arguments
    with pytest.raises(InputError) as e:
        admin_userpermissions_change(token, u_id, permission_id_invalid1)
    with pytest.raises(InputError) as e:
        admin_userpermissions_change(token, u_id, permission_id_invalid2)

    reset_workspace()

def test_user_not_owner(get_permission_id, get_user, get_user2):

    permission_id1 = get_permission_id[0]
    permission_id2 = get_permission_id[1]

    # Add first user into data system so that they are the an owner
    u_id1 = get_user[0]
    assert init_data.USER_DICT[u_id1]["global_permission_id"] == 1
    # Add second user who is just a member
    u_id2, token2 = get_user2
    assert init_data.USER_DICT[u_id2]["global_permission_id"] == 2

    # Check that function throws AccessError if user 2 a(a member) tries to change permissions
    with pytest.raises(AccessError) as e:
        admin_userpermissions_change(token2, u_id2, permission_id1)
    with pytest.raises(AccessError) as e:
        admin_userpermissions_change(token2, u_id2, permission_id2)

    reset_workspace()