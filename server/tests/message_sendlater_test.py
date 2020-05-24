''' File tests the message_sendlater function '''
import pytest
import init_data
import time
from src.error import InputError, AccessError
from src.auth import auth_register
from src.message import message_send, message_sendlater
from src.channels import channels_create
from src.channel import channel_invite
from src.channel import channel_join
from src.workspace import reset_workspace


# Creates a list of users (each being a dictionary)
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

def test_sendlater_invalid_cid(get_5_new_users):
    # Get 5 new users in a list using fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])
    channel_invite(user_1['token'], channel_id, user_5['u_id'])

    message_send(user_1['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_2['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_3['token'], channel_id, "Hey everyone, welcome to thgge channel!")
    message_send(user_4['token'], channel_id, "Hey everyone, welcome tgeo the channel!")
    message_send(user_5['token'], channel_id, "Hey everyone, welcomeee to the channel!")

    time_sent = 1585311430

    # Assume 422 is invalid channel id
    with pytest.raises(InputError) as e:
        message_sendlater(user_3['token'], 422, "YOYOYO", time_sent)

    # messages = init_data.MESSAGES_DICT[channel_id]
    reset_workspace()

def test_sendlater_invalid_time_sent(get_5_new_users):
    # Get 5 new users in a list using fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])
    channel_invite(user_1['token'], channel_id, user_5['u_id'])

    message_send(user_1['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_2['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_3['token'], channel_id, "Hey everyone, welcome to thgge channel!")
    message_send(user_4['token'], channel_id, "Hey everyone, welcome tgeo the channel!")
    message_send(user_5['token'], channel_id, "Hey everyone, welcomeee to the channel!")

    time_sent = 1585311430

    with pytest.raises(InputError) as e:
        message_sendlater(user_3['token'], channel_id, "YOYOYO", time_sent)

    # messages = init_data.MESSAGES_DICT[channel_id]
    reset_workspace()

def test_sendlater_invalid_message_sent(get_5_new_users):
    # Get 5 new users in a list using fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])
    channel_invite(user_1['token'], channel_id, user_5['u_id'])

    message_send(user_1['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_2['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_3['token'], channel_id, "Hey everyone, welcome to thgge channel!")
    message_send(user_4['token'], channel_id, "Hey everyone, welcome tgeo the channel!")
    message_send(user_5['token'], channel_id, "Hey everyone, welcomeee to the channel!")

    time_sent = 1585311430

    with pytest.raises(InputError) as e:
        message_sendlater(user_3['token'], channel_id, "Y"*2000, time_sent)

    # messages = init_data.MESSAGES_DICT[channel_id]
    reset_workspace()

def test_sendlater_user_not_in_channel(get_5_new_users):
    # Get 5 new users in a list using fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])

    message_send(user_1['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_2['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_3['token'], channel_id, "Hey everyone, welcome to thgge channel!")
    message_send(user_4['token'], channel_id, "Hey everyone, welcome tgeo the channel!")

    time_sent = 1585311430

    # User not part of channel
    with pytest.raises(InputError) as e:
        message_sendlater(user_5['token'], channel_id, "Y", time_sent)

    # messages = init_data.MESSAGES_DICT[channel_id]
    reset_workspace()

def test_sendlater_success(get_5_new_users):
    # Get 5 new users in a list using fixture
    users_list = get_5_new_users

    # Assign users to individual variables for easier understanding
    user_1 = users_list[0]
    user_2 = users_list[1]
    user_3 = users_list[2]
    user_4 = users_list[3]
    user_5 = users_list[4]

    # Create a private channel with user_1 as the owner and call it "Standups"
    standups_channel = channels_create(user_1['token'], "Standups", False)

    channel_id = standups_channel['channel_id']

    # Invite all other users to channel with user_1 token 
    channel_invite(user_1['token'], channel_id, user_2['u_id'])
    channel_invite(user_1['token'], channel_id, user_3['u_id'])
    channel_invite(user_1['token'], channel_id, user_4['u_id'])
    channel_invite(user_1['token'], channel_id, user_5['u_id'])

    message_send(user_1['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_2['token'], channel_id, "Hey everyone, welcome to the channel!")
    message_send(user_3['token'], channel_id, "Hey everyone, welcome to thgge channel!")
    message_send(user_4['token'], channel_id, "Hey everyone, welcome tgeo the channel!")
    message_send(user_5['token'], channel_id, "Hey everyone, welcomeee to the channel!")

    time_created = int(time.time())
    time_sent = int(time.time()) + 5

    m_id = message_sendlater(user_3['token'], channel_id, "YO!!", time_sent)

    message_sent_dict = init_data.MESSAGES_DICT[channel_id][0]

    assert message_sent_dict['message_id'] == m_id['message_id']
    assert message_sent_dict['u_id'] == user_3['u_id']
    assert message_sent_dict['message'] == "YO!!"
    assert message_sent_dict['time_created'] == time_created
    assert message_sent_dict['time_sent'] == time_sent

    reset_workspace()