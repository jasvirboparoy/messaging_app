'''
This file contains implementation for auth functions including
register, login and logout
'''
import hashlib
from time import time
from re import search
import jwt
from src.error import InputError, AccessError
from src.user_helper import is_token_valid, is_user_deleted
from src.config import SECRET
import init_data
import string
import random
import smtplib
from email.message import EmailMessage

def hash_password(password):
    '''
    Hashes a given password and returns hash as output
    Input: password string
    Output: hashed password
    '''
    return hashlib.sha256(password.encode()).hexdigest()

def generate_new_u_id():
    '''
    Creates a new u_id
    Input:
    Output: unique u_id generated using uuid1 (integer return)
    '''
    return len(init_data.USER_DICT) + 1

def generate_token(u_id):
    '''
    Generates a token given an email
    Input: u_id
    Output: token
    '''
    iat = time()
    payload = {
        "u_id": u_id,
        "iat": iat
        }
    return jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')

# The following function is from:
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# Author: AnkitRai01
# Slight changes have been made to code to return boolean
def is_email_invalid(email):
    '''
    Function for checking if email is invalid
    Input: Email string
    Output: Boolean
    '''
    # Make a regular expression for validating an Email
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    # pass the regualar expression
    # and the string in search() method
    if search(regex, email):
        # if this condition is true, then email is valid
        # return false
        return False

    # Otherwise the email is invalid
    return True

def is_email_used(entered_email):
    '''
    Function checks whether email is used
    Input: email string
    Output: Boolean (True if email used)
    '''
    # get user dictionary from data store
    users = init_data.USER_DICT

    # create empty list to store emails
    emails = []

    # Put all used emails into emails list
    for key in users:
        emails.append(users[key]['email'])

    # Check if email has been used
    if entered_email in emails:
        return True

    # Return false if email not used
    return False

def is_handle_str_used(handle_str):
    '''
    Function checks whether handle_str is used
    Input:  handle_str
    Output: Boolean (True if handle_str used)
    '''
    # get user dictionary from data store
    users = init_data.USER_DICT

    # create empty list to store handle_str
    handle_str_list = []

    # Put all used handle_str into handle_str_list
    for key in users:
        handle_str_list.append(users[key]['handle_str'])

    # Check if handle_str has been used
    if handle_str in handle_str_list:
        return True

    # Return false if handle_str not used
    return False

def auth_login(email, password):
    '''
    Given registered users details, generate token
    Input: email, password
    Output: {u_id, token}
    '''
    users = init_data.USER_DICT

    # Covert email to store as lowercase
    email = email.lower()

    # Hash a given password for login
    hash_pw = hash_password(password)

    # Email entered is not a valid email
    if is_email_invalid(email):
        raise InputError(description="Invalid email entered")

    # Email entered does not belong to a user
    if not is_email_used(email):
        raise InputError(description="Email doesn't belong to a user")

    # Password is not correct
    for key in users:
        if users[key]['email'] == email:
            u_id = key
            break

    if is_user_deleted(u_id):
        raise AccessError(description="Account has been deleted, contact admin")

    if users[u_id]['password'] != hash_pw:
        raise InputError(description="Password is not correct")

    token = generate_token(u_id)
    init_data.TOKENS_DICT['valid_tokens'][token] = u_id
    return {
        'u_id': u_id,
        'token': token
    }

def auth_logout(token):
    '''
    Logs a user out of system
    Input: token
    Output: is_success
    '''

    if not is_token_valid(token):
        raise AccessError(description="Token is not a valid token")

    tokens_list = init_data.TOKENS_DICT
    for key in tokens_list['valid_tokens']:
        if key == token:
            tokens_list['invalidated_tokens'][token] = tokens_list['valid_tokens'][token]
            del tokens_list['valid_tokens'][token]
            return {
                'is_success': True
                }
    return {
        'is_success': False
        }

def auth_register(email, password, name_first, name_last):
    '''
    Register a new user to system
    Input: email, password, name_first, name_last
    Output: { u_id, token }
    '''

    # Covert email to store as lowercase
    email = email.lower()

    if is_email_invalid(email):
        raise InputError(description="Invalid email was entered")
    if is_email_used(email):
        raise InputError(description="Email is already being used")
    if len(password) < 6:
        raise InputError(description="Password entered was < 6 characters")
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="First name must be between 1 and 50 (inclusive) characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Last name must be between 1 and 50 (inclusive) characters")

    u_id = generate_new_u_id()
    token = generate_token(u_id)
    hashed_password = hash_password(password)

    # All users are consider members (2) except first user
    global_permission_id = 2

    # If there are no users, then they are an owner member (1)
    if len(init_data.USER_DICT) == 0:
        global_permission_id = 1

    handle_str = name_first.lower() + name_last.lower()
    if len(handle_str) > 20:
        handle_str = handle_str[0:20]

    i = 0
    while is_handle_str_used(handle_str):
        handle_str = name_first + str(i)
        if len(handle_str) > 20:
            handle_str = handle_str[-20]
        i += 1


    init_data.USER_DICT[u_id] = {
        'email': email,
        'password': hashed_password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'profile_img_url':"",
        'global_permission_id': global_permission_id,
        'deleted': False
        }

    init_data.TOKENS_DICT['valid_tokens'][token] = u_id

    return {
        'u_id': u_id,
        'token': token
        }
        
#-----------------------------------------------------------------
# below is what i have done
def auth_passwordreset_request(email):
    '''
    Sends a valid reset_code to a valid user email address
    Input: email
    Output: {}
    '''
    # Error thrown if email is invalid
    if given_email_find_u_id(email) == None:
        raise InputError(description="The email entered does not exist in Slackr")
    
    # Generate reset code
    reset_code = generate_random_reset_code()

    # Store email and reset_code in database
    new_reset = {
        'email': email,
        'reset_code': reset_code
    }

    init_data.PASSWORD_RESET.insert(0, new_reset)
    
    # Send reset_code to users email
    from_email = "python.powers.f09a@gmail.com"
    from_pass = "F09APython"

    msg = EmailMessage()
    msg['Subject'] = 'Reset your password'
    msg['From'] = from_email
    msg['To'] = email
    msg.set_content('Dear loyal Slackr user,\n \nYour password reset code is:\n\n' + reset_code)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email, from_pass)
        smtp.send_message(msg)

    return {}
    
def auth_passwordreset_reset(reset_code, new_password):
    '''
    Resets users password if a valid reset_code is entered
    Input: reset_code, new_password
    Output: {}
    '''
    # Check whether reset_code is correct or not
    if not is_reset_in(reset_code):
        raise InputError(description="Reset code entered is not valid")

    # Check whether new_password is valid
    if len(new_password) < 6:
        raise InputError(description="Password entered is less than 6 characters long")
    
    # Check that new_password is not the same as the previous password
    email = given_reset_get_email(reset_code)
    u_id = given_email_find_u_id(email)

    if init_data.USER_DICT[u_id]['password'] == hash_password(new_password):
        raise InputError(description="New password cannot be same as old password")

    # Reset password
    init_data.USER_DICT[u_id]['password'] = hash_password(new_password)

    # Delete reset_code from system
    reset_list = init_data.PASSWORD_RESET
    idx = is_user_idx_reset(reset_code)
    del reset_list[idx]

    return {}

# Helper function: Generates a reset_code for auth_passwordreset_request
def generate_random_reset_code():
    # reset code length
    reset_code_length = 6
    
    # generate random reset code with only numbers and uppercase English letters
    reset_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(reset_code_length))
    while is_reset_in(reset_code):
        reset_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(reset_code_length))
    
    return reset_code

# Helper function: Check that reset_code is not in database
def is_reset_in(reset_code):
    reset_info = init_data.PASSWORD_RESET
    for key in reset_info:
        if key['reset_code'] == reset_code:
            return True
    return False

# Helper function: Given users email, find their u_id
def given_email_find_u_id(email):
    
    for key in init_data.USER_DICT:
        if init_data.USER_DICT[key]['email'] == email:
            return key
    
    raise InputError(description="given email not found")
    
    return

# Helper function: Given a reset_code, get users email
def given_reset_get_email(reset_code):
    reset_info = init_data.PASSWORD_RESET
    for key in reset_info:
        if key['reset_code'] == reset_code:
            email = key['email']
            return email
    return

# Find index of users reset information in database
def is_user_idx_reset(reset_code):
    """
    Check find idx of users reset information in system
    Input: reset_code
    Output:Boolean
    """ 
    reset_list = init_data.PASSWORD_RESET
    idx = -1
    for key in reset_list:
        idx += 1
        if key["reset_code"] == reset_code:
            return idx
    return idx

