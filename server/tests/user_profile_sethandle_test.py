import pytest
from src.user import user_profile, user_profile_sethandle
from src.error import InputError
from src.auth import auth_register
from src.workspace import reset_workspace
'''
    user profile sethandle test
    given(token, handle_str), return {} 
    
    1. invaild handle_str
    2. handle_str is already used by another user
    3. the function is not working
    
    assuming auth_register works
    assuming token is always vaild
'''
# testing use_profile_sethandle function with incorrect inputs
def test_user_profile_sethandle_input_error():
    reset_workspace()
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    # handle_str less then 3 characters
    with pytest.raises(InputError) as e:
        user_profile_sethandle(result['token'], "a")

    # handle_str less then 3 characters
    with pytest.raises(InputError) as e:
        user_profile_sethandle(result['token'], "aa")

    # handle_str greater then 21 characters
    with pytest.raises(InputError) as e:
        user_profile_sethandle(result['token'], "a" * 21)



# handle is already being used
def test_user_profile_sethandle_handle_already_being_used():
    reset_workspace()
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    user_two = auth_register("daniel@gmail.com", "@#asd123!", "daniel", "li")

    user_profile_sethandle(user_one['token'], "aiden")

    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_two['token'], "aiden")


# testing use_profile_sethandle function with correct inputs
def test_user_profile_sethandle():
    reset_workspace()
    
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    user_profile_sethandle(result['token'], "aiden")
    
    user = user_profile(result['token'], result['u_id'])
    
    assert user['handle_str'] == "aiden"
