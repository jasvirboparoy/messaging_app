''' This file contains the data structure for our server '''

# owners, and members has a LIST of u_ids
CHANNELS_DICT = {
    """"c_id":{
        "name":"",
        "owners":[
            {
                "u_id":"",
                "first_name":"",
                "last_name":""
            }
        ],
        "members":[
            {
                "u_id":"",
                "first_name":"",
                "last_name":""
            }
        ],
        "is_public": False,
        "is_standup_active": True,
        "standup": {
            "is_active": True,
            "token_started": "",
            "time_finsh": "",
            "message_buffer": ""
            }
        }
    """
    }

USER_DICT = {
    """
    "u_id":{
        "email":"",
        "password": "",
        "name_first":"",
        "name_last":"",
        "handle_str":"",
        "profile_img_url":"",
        "global_permission_id": 1,
        "deleted": False
        }
    """
    }

MESSAGES_DICT = { 
    
    "c_id": [
        {
            "message_id":"",
            "u_id":"",
            "message":"",
            "time_created":"",
            "reacts":"",
            "is_pinned":False}
        ]
    
        }

TOKENS_DICT = {
    """
    "valid_tokens": {
        "token": "u_id"
        },
    "invalidated_tokens": {
        "token": "u_id"
        }
    """
    }

# STANDUP_DICT = {
#     "c_id": {
#         "message_buffer": "",
#         "starter_token": "",
#         "time_finish": ""
#     }
# }


HANGMAN = {
'''
    "c_id": {
        "word":"",
        "word_template":"",
        "hangman":"",
        "letter_guessed":"",
        "letter_found":"",
        "num_letters_to_guess":"",
        "num_wrong_guesses":"",
    },
'''
}

PASSWORD_RESET = [
    '''{
        'email': '',
        'reset_code': ''
    }'''
]

# Store data in list
DATA_LIST = [CHANNELS_DICT, USER_DICT, MESSAGES_DICT, TOKENS_DICT, HANGMAN, PASSWORD_RESET]


# with open('DATA.pickle', 'wb') as FILE:
    # pickle.dump(DATA_LIST, FILE)

# FILE.close()
