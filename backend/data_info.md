Info for DATA.pickle structure:

Initialise the datastructure using by running init_data.py (remove placeholders)

DATA.pickle is a pickled data structure with contains a LIST of DICTIONARIES
    - this is for ease of pickling and unpickling, as you dont have to worry about the 
    order that items were pickled int

DATA_LIST = [CHANNELS_DICT, USER_DICT, MESSAGES_DICT, TOKENS_DICT]

CHANNELS_DICT contains a dictonary of c_ids with a nested dictonary containing 
information as shown below:
    - c_id (channel_ids)
    - owners (as a list of a dictonary of u_id's, firstname, lastname)
    - members (as a list of a dictonary of u_id's, firstname, lastname)
    - is_public ( as a boolean)

This is a placeholded element for demonstration
CHANNELS_DICT = {"c_id":{"owners":[],"members":[],"is_public": False }}


USER_DICT contains a dictonary of u_ids with a nested dictonary containing 
information as shown below:
    - email (string)
    - password (encrypted string)
    - first_name (string)
    - last_name (string)
    - handle_str
USER_DICT = {"u_id":{"email":"","password": "","first_name":"","last_name":"","handle_str"}}

MESSAGES_DICT contains a dictonary of channel_ids with a list storing message_id and message pairs
    - Messages should be stored CHRONOLOGICALLY 
    - Insert new messages at front?


HOW TO USE PICKLING? - A Quick Guide:

IF YOU WANT TO WRITE TO DATA.PICKLE
 - open the file with write (w) as binary (b) as FILE

with open('DATA.pickle', 'wb') as FILE:
    DATA = pickle.load(FILE)

- access the dictonary you want from the list ( 0 - USER_DICT, 1 - CHANNEL_DICT, 2 - MESSAGES_DICT )
- add to list as shown in example below
    test[0]["test_id"] = {"owners":[123],"members":[123],"is_public": False }
- modify as needed

IF YOU WANT TO READ DATA
DATA = pickle.load(open("DATA.pickle", "rb"))

- likewise with above, access elements as needed