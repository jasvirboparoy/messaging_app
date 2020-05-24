import pytest
from src.user import user_profile, user_profile_setemail
from src.error import InputError
from src.auth import auth_register
from src.workspace import reset_workspace
'''
    user profile setemail test
    given(token, email), return {} 
    
    1. invaild email
    2. email address is already being used
    3. if function is not working
    
    assuming auth_register works
    assuming token is always vaild
'''

# testing use_profile_setemail function with incorrect inputs
def test_user_profile_setemail_input_error():
    reset_workspace()
    
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")

    # missing personal_info or domain
    with pytest.raises(InputError) as e:
        user_profile_setemail(result['token'], "@")

    # missing domain
    with pytest.raises(InputError) as e:
        user_profile_setemail(result['token'], "aiden///32@")

    # missing personal_info
    with pytest.raises(InputError) as e:
        user_profile_setemail(result['token'], "@unsw.edu.au")

    # personal_info contains invaild symbols
    with pytest.raises(InputError) as e:
        user_profile_setemail(result['token'], "a!@#$%^&*()@unsw.edu.au")
    
    # missing @ symbol or domain
    with pytest.raises(InputError) as e:
        user_profile_setemail(result['token'], "1213")

    # incorrect space use
    with pytest.raises(InputError) as e:
        user_profile_setemail(result['token'], " aidenshi@unsw.edu.au")

    # intcorrect space use
    with pytest.raises(InputError) as e:
        user_profile_setemail(result['token'], "aidenshi @unsw.edu.au ")



# email address is already being used
def test_user_profile_setemail_email_being_use():
    reset_workspace()
    
    user_one = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    user_two = auth_register("daniel@gmail.com", "@#asd123!", "daniel", "li")

    with pytest.raises(InputError) as e:
        user_profile_setemail(user_two['token'], "aidenshi@unsw.edu.au")




# testing user_profile_setemail function with correct inputs
def test_user_profile_setemail():
    reset_workspace()
    result = auth_register("aidenshi@unsw.edu.au", "123!@#asd", "aiden", "shi")
    user_profile_setemail(result['token'], "shiaiden@gmail.com")
    
    user = user_profile(result['token'], result['u_id'])

    assert user['email'] == "shiaiden@gmail.com"


