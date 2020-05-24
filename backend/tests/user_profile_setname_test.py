import pytest
from src.user import user_profile, user_profile_setname
from src.error import InputError
from src.auth import auth_register
from src.workspace import reset_workspace
'''
    user profile setname test
    given(token, name_first, name_last), return {} 
    
    1. invaild name_first
    2. invaild name_last
    3. the function is not working
    
    assuming auth_register works
    assuming token is always vaild
'''
# test user profile setname with incorrect inputs
def test_user_profile_setname_input_error():
    reset_workspace()
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
            
    # with no name_first input
    with pytest.raises(InputError) as e:
        user_profile_setname(result['token'], "", "a" * 10)
    
    # with no name_last input
    with pytest.raises(InputError) as e:
        user_profile_setname(result['token'], "a" * 10, "")    
    
    # name_first input length out of range
    with pytest.raises(InputError) as e:
        user_profile_setname(result['token'], "a" * 51, "a" * 10)
    
    # name_last input length out of range
    with pytest.raises(InputError) as e:
        user_profile_setname(result['token'], "a" * 10, "a" * 51)
        

        
# test user profile setname with correct inputs
def test_user_profile_setname():
    reset_workspace()
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    
    user_profile_setname(result['token'], "nedia", "ihs")

    user = user_profile(result['token'], result['u_id'])
    
    assert user['name_first'] == "nedia"
    assert user['name_last'] == "ihs"
    
