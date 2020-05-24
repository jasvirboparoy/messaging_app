import pytest
from src.error import InputError,AccessError
from src.channel import channel_invite, channel_join
from src.channels import channels_create
from src.auth import auth_register
from src.workspace import reset_workspace

# testing the general functionality of channels create - can it create 
# a normal channel and then is it possible to join the channel - tests
# assumes auth_register works 
# assumes channel_join works

def test_channels_create():
    # assume that channel_join works, and channel is public
    reset_workspace()
    results = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = channels_create(results["token"],"testchannel",True)

    channel_join(results["token"], c_id["channel_id"])

# assume channels will not be able to created with same name
def test_channels_create_double():
    reset_workspace()
    results = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = channels_create(results["token"],"testchannel2",False)

    with pytest.raises(InputError) as e:
        channels_create(results["token"],"testchannel2",False)

    with pytest.raises(InputError) as e:
        channels_create(results["token"],"testchannel2",True)

# assume created public channels will not be able to be created with same 
# name as created private channel and vice versa

def test_channels_create_double2():
    reset_workspace()
    results = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = channels_create(results["token"],"testchannel3",True)
    with pytest.raises(InputError) as e:
        channels_create(results["token"],"testchannel3",False)

def test_channels_create_double3():
    reset_workspace()
    results = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    c_id = channels_create(results["token"],"testchannel4",True)
    with pytest.raises(InputError) as e:
        channels_create(results["token"],"testchannel4",True)


# function is testing failures for create channel -  
def test_create_fails():
    reset_workspace()
    results1 = auth_register("ernest.yee@gmail.com", "abcdEF12", "Ernest", "Yee")

    # testing a channel with name more then 20 characters
    #1
    with pytest.raises(InputError) as e:
        channels_create(results1["token"], "a" * 21, True)
    #2 longer
    with pytest.raises(InputError) as e:
        channels_create(results1["token"], "a" * 1000, True)
    #3 special characters
    with pytest.raises(InputError) as e:
        channels_create(results1["token"], "!" * 21, True)
    #3 spaces
    with pytest.raises(InputError) as e:
        channels_create(results1["token"], " " * 21, True)
    