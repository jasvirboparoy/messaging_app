# TESTER FILE # RENAME FILE "_test"
import pytest
import init_data
from src.error import InputError, AccessError
from src.auth import auth_passwordreset_request, auth_register
from src.workspace import reset_workspace
import email 
import imaplib

# This file tests the functionality of the function auth_passwordreset_request

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

@pytest.fixture
def register_users():
    auth_register("catpotter18@gmail.com", "123456", "Cat", "Potter")
    auth_register("catherine.thuy.trinh@gmail.com", "654321", "Catherine", "Trinh")
    return ["catpotter18@gmail.com", "catherine.thuy.trinh@gmail.com"]

# Email address is not in database
def test_authpasssword_request_invalid_email():
    # Testing error is thrown if email does not exist in system
    email = "jn92ebdh89135451324nvdsis@gmail.com"

    users = init_data.USER_DICT
    for key in users:
        assert users[key]["email"] != email

    with pytest.raises(AccessError) as e:
        auth_passwordreset_request(email)
    
    reset_workspace()

# Checks data store is updated and email has been sent
def test_authpasssword_request_function(register_users):
    email = register_users[0]
    auth_passwordreset_request(email)
    assert init_data.PASSWORD_RESET[0]["email"] == email
    assert init_data.PASSWORD_RESET[0]["reset_code"] == get_reset_code()

# Checks auth_passwordreset_request works multiple times
def test_authpasssword_request_function(register_users):
    email_1 = register_users[0]
    email_2 = register_users[1]
    
    # First user requests password reset
    auth_passwordreset_request(email_1)
    assert init_data.PASSWORD_RESET[0]["email"] == email_1
    assert init_data.PASSWORD_RESET[0]["reset_code"] == get_reset_code()

    # First user requests password reset
    auth_passwordreset_request(email_1)
    assert init_data.PASSWORD_RESET[0]["email"] == email_2
    assert init_data.PASSWORD_RESET[0]["reset_code"] == get_reset_code()