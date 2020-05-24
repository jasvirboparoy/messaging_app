import pytest
import init_data
from src.error import InputError
from src.auth import auth_register
from src.workspace import reset_workspace

# This file tests the auth_register function 

# auth_register takes in email, password, name_first and name_last 
# It returns a u_id and a token


# CASES:

# Email entered is invalid
def test_auth_register_invalid_email():
    reset_workspace()
    
    # personal_info provided, but no domain or @ symbol
    with pytest.raises(InputError) as e:
        auth_register("hello", "123456Jasvir", "Jasvir", "Boparoy")

    # domain provided but no personal_info
    with pytest.raises(InputError) as e:
        auth_register("@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")

    # personal_info provided as number but no domain or @ symbol
    with pytest.raises(InputError) as e:
        auth_register("1", "123456Jasvir", "Jasvir", "Boparoy")

    # @ symbol seperator provided but no personal_info or domain
    with pytest.raises(InputError) as e:
        auth_register("@", "123456Jasvir", "Jasvir", "Boparoy")
    
    # @ symbol provided and personal_info provided but no domain
    with pytest.raises(InputError) as e:
        auth_register("///32@", "123456Jasvir", "Jasvir", "Boparoy")

    # Leading space
    with pytest.raises(InputError) as e:
        auth_register(" johnsmith@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")

    # Trailing space
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com ", "123456Jasvir", "Jasvir", "Boparoy")


# Email address is already being used by another user
def test_auth_register_taken_email():
    reset_workspace()

    auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")

    # Testing using taken email but different password and name
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "111111145Jasvir", "John", "Smith")

    # Testing using taken email with exactly same name and password
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")


# Password entered is less than 6 characters long
# Passwords of less than 6 characters are invalid
def test_auth_register_invalid_password():
    reset_workspace()

    # Testing numerical password < 6 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "12345", "Jasvir", "Boparoy")

    # Testing lettered password < 6 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "abcd", "Jasvir", "Boparoy")

    # Testing lettered and numerical password < 6 character
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "ab123", "Jasvir", "Boparoy")
    
    # Testing numbers, capital and lowercase letter password < 6 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "Aa1Bb", "Jasvirb", "Boparoy")
    
    # Testing special characters < 6 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "@@@@/", "Jasvir", "Boparoy")
    
    # Testing a combination of characters < 6 characters in length
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "A1b@", "Jasvir", "Boparoy")


# name_first is not between 1 and 50 characters in length
def test_auth_register_invalid_first():
    reset_workspace()

    # Test for name_first with 0 character
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "", "Boparoy")

    # Test for name_first with 51 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "J" * 51, "Boparoy")

    # Test for name_first with 100 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "J" * 100, "Boparoy")


# name_last is not between 1 and 50 characters in length
def test_auth_register_invalid_last():
    reset_workspace()

    # Test for name_last with 0 character
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "")
    
    # Test for name_last with 51 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "B" * 51)
    
    # Test for name_last with 100 characters
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "B" * 100)


# Combination of incorrectly entered values (e.g. multiple incorrect cases)
def test_auth_register_invalid_combination():
    reset_workspace()

    # Test for invalid email, password, first and last name
    with pytest.raises(InputError) as e:
        auth_register("@", "1234", "", "B" * 51)
    
    # Test for invalid password and first name
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123", "J" * 100, "Boparoy")
    
    # Test for invalid names
    with pytest.raises(InputError) as e:
        auth_register("johnsmith@gmail.com", "123456Jasvir", "", "N" * 51)


# SUCCESS CASE
# Valid email entered
# Entered long enough password (>= 6 characters)
# first and last name are less than 50 characters in length each
def test_auth_register_successful():
    reset_workspace()

    # Test valid email, password, first and last names (shouldn't throw error)
    user = auth_register("johnsmith@gmail.com", "123456Jasvir", "Jasvir", "Boparoy")

    u_id = user['u_id']

    # Test that global permission id is 1
    assert init_data.USER_DICT[u_id]['global_permission_id'] == 1

    user2 = auth_register("james@gmail.com", "123456Jfeasvir", "Jall", "Bopy")
    u_id2 = user2['u_id']
    assert init_data.USER_DICT[u_id2]['global_permission_id'] == 2

    user3 = auth_register("jamesww@gmail.com", "123456Jefeasvir", "Jafll", "Boepy")
    u_id3 = user3['u_id']
    assert init_data.USER_DICT[u_id3]['global_permission_id'] == 2