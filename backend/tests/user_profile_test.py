import pytest
from src.user import user_profile, user_profile_sethandle
from src.error import InputError
from src.auth import auth_register
from src.workspace import reset_workspace

''' user profile test
    given(token, u_id), return {emial, name_first, name_last, handle_str} 
   
    1. invalid u_id
    2. if function is not working

assuming auth_register works
assuming user_profile_sethandle works
assuming token is always vaild
'''
# testing use_profile function with incorrect inputs
def test_user_profile_input_error():
    reset_workspace()
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    
    # test for invaild u_id
    with pytest.raises(InputError) as e:
        user_profile(result['token'], -1)
    


# testing use_profile function with correct inputs
def test_use_profile():
    reset_workspace()
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    
    user_profile_sethandle(result['token'], "comp1531")
    
    # test for all vaild case
    assert(user_profile(result['token'], result['u_id'])['email'] == "aidenshi@unsw.edu.au")
    assert(user_profile(result['token'], result['u_id'])['name_first'] == "aiden")
    assert(user_profile(result['token'], result['u_id'])['name_last'] == "shi")
    assert(user_profile(result['token'], result['u_id'])['u_id'] == result['u_id'])
    assert(user_profile(result['token'], result['u_id'])['handle_str'] == "comp1531")



