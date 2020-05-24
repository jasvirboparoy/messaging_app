import pytest
import init_data
from src.auth import auth_passwordreset_reset, auth_passwordreset_request, generate_random_reset_code, auth_register, auth_login
from src.error import InputError, AccessError
from src.workspace import reset_workspace
# from time import sleep
import email 
import imaplib

# This function tests the functionality of auth_passwordreset_reset

# ASSUMPTIONS
# Assume that new password cannot be the same as the previous password
# Unique reset code is deleted from database once used

# Can be added to helper file as a helper function
def get_reset_code():
    # Logging into slackr sender gmail
    username = "python.powers.f09a@gmail.com"
    password = "F09APython"
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)

    # Looking into list of sent mail
    mail.select('"[Gmail]/Sent Mail"')
    result, data = mail.uid('search', None, "ALL")
    sentmail_item_list = data[0].split()

    restult2, email_data = mail.uid('fetch', sentmail_item_list[-1], '(RFC822)')
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)

    for part in email_message.walk():
        content_type = part.get_content_type()
        if "plain" in content_type:
            msg_string = part.as_string()
            e_reset_code = msg_string.split()[-1]
    
    return e_reset_code

# Helper function: Check that reset_code is not in database
def is_reset_in(reset_code):
    reset_info = init_data.PASSWORD_RESET
    for key in reset_info:
        if key['reset_code'] == reset_code:
            return True
    return False

# invalid reset_code is entered
def test_auth_passwordreset_reset_invalid_code():
    reset_workspace()
    # Reset code is not in database
    invalid_code = '123456'
    assert not is_reset_in(invalid_code)
    with pytest.raises(InputError) as e:
        auth_passwordreset_reset(invalid_code, "Password5")

# Invalid password is entered
def test_auth_passwordreset_reset_invalid_password():
    reset_workspace()

    # Register user and request password reset
    auth_register("catherine.thuy.trinh@gmail.com", "123456", "Catherine", "Trinh")
    auth_passwordreset_request("catherine.thuy.trinh@gmail.com")

    # Obtain reset code sent to email
    reset_code = get_reset_code()

    # Password is less than 6 characters
    with pytest.raises(InputError) as e:
        auth_passwordreset_reset(reset_code, "TWO")

# Password is the same as previously set password
def test_auth_passwordreset_reset_password_same():
    reset_workspace()

    # Register user and request password reset
    user = auth_register("catherine.thuy.trinh@gmail.com", "123456", "Catherine", "Trinh")
    auth_passwordreset_request("catherine.thuy.trinh@gmail.com")

    # Obtain reset code sent to email
    reset_code = get_reset_code()
    
    old_password = init_data.USER_DICT[user['u_id']]['password']
    # Password is same as previous password
    with pytest.raises(InputError) as e:
        auth_passwordreset_reset(reset_code, "123456")

    # TEST
    # Check that new_password is not the same as the previous password
    init_data.USER_DICT[user['u_id']]['password'] == old_password

# Checks that password has been reset
def test_auth_passwordreset_reset():  
    reset_workspace()

    # Register user and request password reset
    user = auth_register("catherine.thuy.trinh@gmail.com", "123456", "Catherine", "Trinh")
    auth_passwordreset_request("catherine.thuy.trinh@gmail.com")
    
    # User resets password
    reset_code = get_reset_code()
    auth_passwordreset_reset(reset_code, "654321")
    
    assert init_data.USER_DICT[user['u_id']]['password'] == '654321'

# Check that reset code is deleted from database once used
def test_auth_passwordreset_reset():
    reset_workspace()

    # Register user and request password reset
    user = auth_register("catherine.thuy.trinh@gmail.com", "123456", "Catherine", "Trinh")
    auth_passwordreset_request("catherine.thuy.trinh@gmail.com")
    
    # User resets password
    emailed_reset_code = get_reset_code()
    auth_passwordreset_reset(emailed_reset_code, "654321")
    
    # After 1 second check that reset_code is no longer in database
    # sleep(1)
    assert not is_reset_in(emailed_reset_code)

""" # Check that user can login with new password
def test_auth_passwordreset_reset_login():
    reset_code = generate_random_reset_code()
    init_data.RESET_CODE['email'] = 'z5255218@unsw.edu.au'
    init_data.RESET_CODE['reset_code'] = reset_code
    
    # register a user
    user = auth_register("z5255218@unsw.edu.au", "123!@#asd", "aiden", "shi")
    
    # reset password
    auth_passwordreset_reset(reset_code, 'iamthebest')
    
    assert init_data.USER_DICT[user['u_id']]['password'] == 'iamthebest'
    
    # After 2 seconds check that user can login with new password
    sleep(2)
    assert auth_login('z5255218@unsw.edu.au', 'iamthebest') not None

    # Do function to use token to check that auth_login works

result = auth_register("catpotter18@gmail.com", "123456", "Cat", "Trinh" )
auth_logout(result["token"])
auth_login("catpotter18@gmail.com", "654321")"""
