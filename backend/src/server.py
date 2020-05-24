''' This file contains functions for server '''
import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from persist import save_data, load_data
from auth import auth_login, auth_logout, auth_register, auth_passwordreset_request, auth_passwordreset_reset
from channel import (channel_details, channel_messages, channel_invite, channel_leave,
                     channel_join, channel_addowner, channel_removeowner)
from channels import channels_list, channels_listall, channels_create
from message import (message_send, message_sendlater,
                     message_remove, message_edit)
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from user_profilephoto import user_profile_uploadphoto
from users import users_all
from other import search
# from standups import standup_start, standup_active, standup_send
# from message import message_react, message_unreact, message_pin, message_unpin
from admin import admin_userpermissions_change, admin_user_remove
from workspace import reset_workspace
import distutils.util
from werkzeug.exceptions import HTTPException
import os
def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.config['IMAGE_FOLDER'] = os.path.abspath(os.getcwd())
APP.register_error_handler(Exception, defaultHandler)

# Example
# This is one type of route
# @APP.route("/echo", methods=['GET'])
# def echo():
#     data = request.args.get('data')
#     if data == 'echo':
#    	    raise InputError(description='Cannot echo "echo"')
#     return dumps({
#         'data': data
#     })

# ========== auth.py functions ================
@APP.route("/auth/login", methods=['POST'])
def login_user_http():
    '''
    Logs a user in
    Input: (email, password)
    Output: { u_id, token }
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    output_dict = auth_login(email, password)
    return dumps(output_dict)

@APP.route("/auth/logout", methods=['POST'])
def logout_user_http():
    '''
    Logs a user out
    Input: (token)
    Output: { is_success }
    '''
    payload = request.get_json()
    token = payload['token']
    output = auth_logout(token)
    return dumps(output)

@APP.route("/auth/register", methods=['POST'])
def register_user_http():
    '''
    Flask route to register a new user to system
    Input: (email, password, name_first, name_last)
    Output: { u_id, token }
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    output = auth_register(email, password, name_first, name_last)
    return dumps(output)


@APP.route("/auth/passwordreset/request", methods=['POST'])
def passwordreset_request_http():
    '''
    Send reset_code to user
    Input: (email)
    Output: {}
    '''
    payload = request.get_json()
    email = payload['email']
    output = auth_passwordreset_request(email)
    return dumps(output)


@APP.route("/auth/passwordreset/reset", methods=['POST'])
def passwordreset_reset_http():
    '''
    Check if reset_code is vaild, if ture change the password for current user
    Input: (reset_code, new_password)
    Output: {}
    '''
    payload = request.get_json()
    reset_code = payload['reset_code']
    new_password = payload['new_password']
    output = auth_passwordreset_reset(reset_code, new_password)
    return dumps(output)



# ================== Channel.py Functions ======================

@APP.route("/channel/invite", methods=['POST'])
def channel_invite_http():
    '''
    Flask route to invite a user to a channel
    Input: (token, channel_id, u_id)
    Output: {}
    '''
    payload = request.get_json()
    token = payload["token"]
    c_id = int(payload["channel_id"])
    u_id = int(payload["u_id"])
    output = channel_invite(token, c_id, u_id)
    return dumps(output)

@APP.route("/channel/details", methods=['GET'])
def channel_details_http():
    '''
    Gets basic details of channel
    Input: (token, channel_id)
    Output: { name, owner_members, all_members }
    '''
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    output = channel_details(token, channel_id)
    print (output)
    return dumps(output)

@APP.route("/channel/messages", methods=['GET'])
def channel_messages_http():
    '''
    Gets the messages for channel
    Input: (token, channel_id, start)
    Output: { messages, start, end }
    '''
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    output = channel_messages(token, channel_id, start)
    print (output)
    return dumps(output)

@APP.route("/channel/leave", methods=['POST'])
def channel_leave_http():
    """
    Flask route to leave a channel
    Input: token, channel_id
    Output: {}
    """
    payload = request.get_json()
    token = payload["token"]
    channel_id = int(payload['channel_id'])
    output = channel_leave(token,channel_id)
    return dumps(output)

@APP.route("/channel/join", methods=['POST'])
def channel_join_http():
    """
    Flask route to join a channel
    Input: token, channel_id
    Output: {}
    """
    payload = request.get_json()
    token = payload["token"]
    channel_id = int(payload['channel_id'])
    print(channel_id)
    output = channel_join(token, channel_id)
    return dumps(output)

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner_http():
    """
    Flask route to add an owner to channel
    Input: token, channel_id, u_id
    Output: {}
    """
    payload = request.get_json()
    token = payload["token"]
    channel_id = int(payload['channel_id'])
    u_id = int(payload["u_id"])
    output = channel_addowner(token,channel_id,u_id)
    return dumps(output)
    
@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner_http():
    """
    Flask route to remove an owner from channel
    Input: token, channel_id, u_id
    Output: {}
    """
    payload = request.get_json()
    token = payload["token"]
    channel_id = int(payload['channel_id'])
    u_id = int(payload["u_id"])
    output = channel_removeowner(token, channel_id, u_id)
    return dumps(output)

# ============== Channels.py Functions ======================

@APP.route("/channels/list", methods=['GET'])
def channels_list_http():
    """
    Flask route to list all channels
    Input: (token)
    Output: { channels }
    """
    token = request.args.get('token')
    channels = channels_list(token)
    return dumps(channels)

@APP.route("/channels/listall", methods=['GET'])
def channels_listall_http():
    '''
    Provides list of all channels and details
    Input: (token)
    Output: { channels }
    '''
    token = request.args.get('token')
    print(token)
    channels = channels_listall(token)
    return dumps(channels)

@APP.route("/channels/create", methods=['POST'])
def channels_create_http():
    '''
    Creates new channel
    Input: (token, name, is_public)
    Output: { channel_id }
    '''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload["is_public"]

    channel_id = channels_create(token, name, is_public)
    return dumps(channel_id)

# ============== messages.py Functions ======================
@APP.route("/message/send", methods=['POST'])
def message_send_http():
    '''
    Sends a message in a channel
    Input: (token, channel_id, message)
    Output: { message_id }
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    message_id = message_send(token, channel_id, message)
    return dumps(message_id)

@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater_http():
    '''
    Sends message at given time
    Input: (token, channel_id, message, time_sent)
    Output: { message_id }
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    time_sent = int(payload['time_sent'])
    message_id_dict = message_sendlater(token, channel_id, message, time_sent)
    return dumps(message_id_dict)

# Not important right now
# @APP.route("/message/react", methods=['POST'])
# def message_react_http():
#     '''
#     Reacts to a message
#     Input: (token, message_id, react_id)
#     Output: {}
#     '''
#     payload = request.get_json()
#     token = payload['token']
#     message_id = payload['message_id']
#     react_id = payload['react_id']
#     message_react(token, message_id, react_id)
#     return dumps({})

# Not important right now
# @APP.route("/message/unreact", methods=['POST'])
# def message_unreact_http():
#     '''
#     Unreacts to a message
#     Input: (token, message_id, react_id)
#     Output: {}
#     '''
#     payload = request.get_json()
#     token = payload['token']
#     message_id = payload['message_id']
#     react_id = payload['react_id']
#     returned = message_unreact(token, message_id, react_id)
#     return dumps(returned)

# Not important right now
# @APP.route("/message/pin", methods=['POST'])
# def message_pin_http():
#     '''
#     Pins a message
#     Input: (token, message_id)
#     Output: {}
#     '''
#     payload = request.get_json()
#     token = payload['token']
#     message_id = payload['message_id']
#     returned = message_pin(token, message_id)
#     return dumps(returned)

# Not important right now
# @APP.route("/message/unpin", methods=['POST'])
# def message_unpin_http():
#     '''
#     Unpins a message
#     Input: (token, message_id)
#     Output: {}
#     '''
#     payload = request.get_json()
#     token = payload['token']
#     message_id = payload['message_id']
#     returned = message_unpin(token, message_id)
#     return dumps(returned)

@APP.route("/message/remove", methods=['DELETE'])
def message_remove_http():
    '''
    Removes a message from channel
    Input: (token, message_id)
    Output: {}
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    returned = message_remove(token, message_id)
    return dumps(returned)

@APP.route("/message/edit", methods=['PUT'])
def message_edit_http():
    '''
    Edits a message
    Input: (token, message_id, message)
    Output: {}
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    message = payload['message']
    returned = message_edit(token, message_id, message)
    return dumps(returned)

# ============== user.py Functions ======================
@APP.route("/user/profile", methods=['GET'])
def user_profile_http():
    '''
    Gets info about user
    Input: (token, u_id)
    Output: { user }
    '''
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    returned = user_profile(token, u_id)
    return dumps(returned)

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname_http():
    '''
    Sets the name for user
    Input: (token, name_first, name_last)
    Output: {}
    '''
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    returned = user_profile_setname(token, name_first, name_last)
    return dumps(returned)

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail_http():
    '''
    Sets email for user
    Input: (token, email)
    Output: {}
    '''
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    returned = user_profile_setemail(token, email)
    return dumps(returned)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle_http():
    '''
    Sets handle for user
    Input: (token, handle_str)
    Output: {}
    '''
    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']
    returned = user_profile_sethandle(token, handle_str)
    return dumps(returned)

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_uploadphoto_http():
    '''
    Given url, crops it and puts on server
    Input: (token, img_url, x_start, y_start, x_end, y_end)
    Output: {}
    '''
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    x_start = int(payload['x_start'])
    y_start = int(payload['y_start'])
    x_end = int(payload['x_end'])
    y_end = int(payload['y_end'])
    returned = user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
    return returned

@APP.route("/get_image/<path:filename>")
def get_image(filename):

    try:
        return send_from_directory(APP.config["IMAGE_FOLDER"], filename=filename, as_attachment=False)
    except FileNotFoundError:
        raise(HTTPException)

@APP.route("/users/all", methods=['GET'])
def users_all_http():
    '''
    Gets a list of all users
    Input: (token)
    Output: { users}
    '''
    token = request.args.get('token')
    returned = users_all(token)
    return dumps(returned)

# ====== search.py functions??? ======
# Located in other.py
@APP.route("/search", methods=['GET'])
def search_http():
    '''
    Searches for messages
    Input: (token, query_str)
    Output: { messages }
    '''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    messages_dict = search(token, query_str)
    return dumps(messages_dict)

# STANDUPS NOT DONE
@APP.route("/standup/start", methods=['POST'])
def standup_start_http():
    '''
    Starts a new standup
    Input: (token, channel_id, length)
    Output: { time_finish }
    '''
    # payload = request.get_json()
    # token = payload['token']
    # channel_id = int(payload['channel_id'])
    # length = payload['length']
    # time_finish_dict = standup_send(token, channel_id, length)
    # return dumps(time_finish_dict)
    return dumps({})

@APP.route("/standup/active", methods=['GET'])
def standup_active_http():
    '''
    Checks whether standup is active
    Input: (token, channel_id)
    Output: { is_active, time_finish }
    '''
    # token = request.args.get('token')
    # channel_id = request.args.get('channel_id')
    # returned_dict = standup_active(token, channel_id)
    # return dumps(returned_dict)
    return dumps({})

@APP.route("/standup/send", methods=['POST'])
def standup_send_http():
    '''
    Sends a standup to channel
    Input: (token, channel_id, message)
    Output: {}
    '''
    # payload = request.get_json()
    # token = payload['token']
    # channel_id = int(payload['channel_id'])
    # message = payload['message']
    # returned = standup_send(token, channel_id, message)
    # return dumps(returned)
    return dumps({})

# ============= admin.py functions =====================
# admin_userpermission_change.py
@APP.route("/admin/userpermission/change", methods=['POST'])
def change_userpermission_http():
    '''
    Change the user permision of another user
    Input: (token, u_id, permission_id)
    Output: {}
    '''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    returned = admin_userpermissions_change(token, u_id, permission_id)
    return dumps(returned)

@APP.route("/admin/user/remove", methods=['DELETE'])
def admin_user_remove_http():
    '''
    Removes a user from slackr
    Input: (token, u_id)
    Output: {}
    '''
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))

    returned = admin_user_remove(token, u_id)

    return dumps(returned)

# ============= workspace.py function ===================
@APP.route("/workspace/reset", methods=['POST'])
def reset_workspace_http():
    '''
    Resets the database to remove everything
    Input: ()
    Output: {}
    '''
    reset_workspace()
    return dumps({})

if __name__ == "__main__":
    load_data()
    save_data()
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
