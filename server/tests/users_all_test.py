import pytest
from src.user import user_profile, user_profile_sethandle
from src.error import InputError
from src.auth import auth_register
from src.users import users_all
from src.workspace import reset_workspace
import init_data
'''
    users_all test
    given(token), return{users}

    assuming user_profile works
    assuming auth_register works
    assuming token is always vaild
'''

def test_users_all():
    reset_workspace()
    # register three users
    user1 = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    user2 = auth_register("danielli@gmail.com", "12@#asd3!", "danile", "li")
    user3 = auth_register("andrewchen@unsw.edu.au", "@#asd123!123!", "andrew", "chen")

    # set handle for each user
    user_profile_sethandle(user1['token'], "aidenshi")
    user_profile_sethandle(user2['token'], "danielli")
    user_profile_sethandle(user3['token'], "andrewchen")

    # assign user list
    user_list = users_all(user1['token'])
    user_list_two = users_all(user2['token'])
    user_list_three = users_all(user3['token'])

    # all list should be the same
    assert user_list == user_list_two
    assert user_list_two == user_list_three

    u_ids = u_id_list()
    assert user_list == {
        'users' : [
            {
                "u_id" : u_ids[0],
                "email" : "aidenshi@unsw.edu.au",
                "name_first" : "aiden",
                "name_last" : "shi",
                "handle_str" : "aidenshi"
            },
            
            {
                "u_id" : u_ids[1],
                "email" : "danielli@gmail.com",
                "name_first" : "danile",
                "name_last" : "li",
                "handle_str" : "danielli"
            },
            
            {
                "u_id" : u_ids[2],
                "email" : "andrewchen@unsw.edu.au",
                "name_first" : "andrew",
                "name_last" : "chen",
                "handle_str" : "andrewchen"
            }
        
        ]
    }

def u_id_list():
    u_id = []
    for key in init_data.USER_DICT:
        u_id.append(key)
    return u_id
