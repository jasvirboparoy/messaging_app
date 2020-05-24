import pytest
from src.auth import auth_register, auth_logout, auth_login
from src.error import AccessError
from src.workspace import reset_workspace


# This file contains test functions that test auth_logout functionality
# auth_logout takes in a token (string) and returns is_success (boolean)

# These tests assume that auth_register works and auth_login works

# This function tests whether auth_logout function handles valid token case correctly
def test_auth_logout_valid_token():
    reset_workspace()

    # Register a new user
    user = auth_register("jasvirboparoy@gmail.com", "helloWorld1234", "Jasvir", "Boparoy")
    user_id = user['u_id']

    login_user = auth_login("jasvirboparoy@gmail.com", "helloWorld1234")
    login_user_id = login_user['u_id']

    # Ensure this is the same user that registered and has now logged in
    assert user_id == login_user_id

    token = login_user['token']

    # Check that logout invalidated token for active user
    assert (auth_logout(token))['is_success'] == True

# This function tests whether function returns access error for an invalid token
def test_auth_logout_invalid_token():
    reset_workspace()
    
    # Create a fake token that is invalid
    token_1 = "1234573331jasvirB"

    # logging out fake token should throw an access error
    with pytest.raises(AccessError) as e:
        auth_logout(token_1)

    # Token 2 uses 4 spaces only
    token_2 = "    "

    # Using token 2 should throw access error
    with pytest.raises(AccessError) as e:
        auth_logout(token_2)
