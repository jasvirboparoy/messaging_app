''' This file contains functions to reset the workspace '''

import init_data

def reset_workspace():
    '''
    Reset the workspace data to original form
    '''
    init_data.CHANNELS_DICT = {}
    init_data.USER_DICT = {}
    init_data.MESSAGES_DICT = {}
    init_data.TOKENS_DICT = {
        'valid_tokens': {},
        'invalidated_tokens': {},
        }
    init_data.PASSWORD_RESET = []
    init_data.HANGMAN = {}
