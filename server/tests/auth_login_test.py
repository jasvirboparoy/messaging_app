import pytest
from src.error import InputError
from src.auth import auth_register, auth_login
from src.workspace import reset_workspace

# Testing the auth_login function

# auth_login takes email and password as parameters
# Returns u_id and token in dictionary

# ====== ASSUMPTIONS FOR THESE TESTS =========
# Assume auth_register works


# Function tests cases of invalid email entered for log in
def test_auth_login_invalid_email():
    reset_workspace()

    # Register a user
    user = auth_register("jasvirboparoy@gmail.com", "helloWorld", "Jasvir", "Boparoy")

    # personal_info provided, but no domain or @ symbol
    with pytest.raises(InputError) as e:
        auth_login("hello", "123456Hello")

    # domain provided but no personal_info
    with pytest.raises(InputError) as e:
        auth_login("@gmail.com", "1222455Hello")

    # personal_info provided as number but no domain or @ symbol
    with pytest.raises(InputError) as e:
        auth_login("1", "1234567Jb")

    # @ symbol seperator provided but no personal_info or domain
    with pytest.raises(InputError) as e:
        auth_login("@", "1234567Jb")
    
    # @ symbol provided and personal_info provided but no domain
    with pytest.raises(InputError) as e:
        auth_login("///32@", "1234567Jb")

    # Leading space
    with pytest.raises(InputError) as e:
        auth_login(" jasvirboparoy@gmail.com", "helloWorld")

    # Trailing space
    with pytest.raises(InputError) as e:
        auth_login("jasvirboparoy@gmail.com ", "helloWorld")


# Function tests cases where email provided doesn't belong to a user
def test_auth_login_unregistered_email():

    # Using valid email to login but hasn't been registered
    with pytest.raises(InputError) as e:
        auth_login("jasvir@gmail.com", "helloWorld")

    with pytest.raises(InputError) as e:
        auth_login("hello@email.com", "helloWorld")

# Function tests cases where email has been registered and entered email
# matches for log in. It should not throw an exception
def test_auth_login_registered_email():
    reset_workspace()

    user = auth_register("jasvirboparoy@gmail.com", "helloWorld", "Jasvir", "Boparoy")
    u_id = user['u_id']
    token = user['token']
   
    # Using all caps for a valid email that has been registered in lowercase
    result_1 = auth_login("JASVIRBOPAROY@GMAIL.COM", "helloWorld")

    assert result_1['u_id'] == u_id
    # assert result_1['token'] == token (invalid to check this)

    # Using first letter capitalised for valid email that's registered
    result_2 = auth_login("Jasvirboparoy@gmail.com", "helloWorld")

    assert result_2['u_id'] == u_id
    # Invalid to test this as new token for each session
    # assert result_2['token'] == token


# Function tests cases where incorrect password has been typed
def test_auth_login_incorrect_password():
    reset_workspace()

    user = auth_register("jasvirboparoy@gmail.com", "HELLOWORLD1124", "Jasvir", "Boparoy")

    # registered with all caps, entered all lowercase
    with pytest.raises(InputError) as e:
        auth_login("jasvirboparoy@gmail.com", "helloworld1124")

    # Completely wrong password entered
    with pytest.raises(InputError) as e:
        auth_login("jasvirboparoy@gmail.com", "123456Hello")
    
    # Entered one character with wrong case
    with pytest.raises(InputError) as e:
        auth_login("jasvirboparoy@gmail.com", "hELLOWORLD1124")

    # Entered leading space for valid password
    with pytest.raises(InputError) as e:
        auth_login("jasvirboparoy@gmail.com", " HELLOWORLD1124")

    # Entered trailing space for valid password
    with pytest.raises(InputError) as e:
        auth_login("jasvirboparoy@gmail.com", "HELLOWORLD1124 ")

# Function tests cases where correct password has been entered
def test_auth_login_correct_password():
    reset_workspace()
    
    user = auth_register("jasvirboparoy@gmail.com", "HELLOWORLD1124", "Jasvir", "Boparoy")
    u_id = user['u_id']
    token = user['token']

    user_login = auth_login("jasvirboparoy@gmail.com", "HELLOWORLD1124")
    user_login_u_id = user_login['u_id']
    user_login_token = user_login['token']

    assert u_id == user_login_u_id
    # Invalid to test this as new token for new session
    # assert token == user_login_token
