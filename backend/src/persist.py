''' This file contains the saving and loading functions '''
import threading
import pickle
import init_data
from workspace import reset_workspace

def load_data():
    '''
    loads the data from json files
    '''
    try:
        data = pickle.load(open('channels_dict.p', 'rb'))
        init_data.CHANNELS_DICT = data
    except FileNotFoundError:
        reset_workspace()
        data = init_data.CHANNELS_DICT
        pickle.dump(data, open('channels_dict.p', 'wb'))
    try:
        data = pickle.load(open('user_dict.p', 'rb'))
        init_data.USER_DICT = data
    except FileNotFoundError:
        reset_workspace()
        data = init_data.USER_DICT
        pickle.dump(data, open('user_dict.p', 'wb'))
    try:
        data = pickle.load(open('messages_dict.p', 'rb'))
        init_data.MESSAGES_DICT = data
    except FileNotFoundError:
        reset_workspace()
        data = init_data.MESSAGES_DICT
        pickle.dump(data, open('messages_dict.p', 'wb'))
    try:
        data = pickle.load(open('tokens_dict.p', 'rb'))
        init_data.TOKENS_DICT = data
    except FileNotFoundError:
        reset_workspace()
        data = init_data.TOKENS_DICT
        pickle.dump(data, open('tokens_dict.p', 'wb'))
    try:
        data = pickle.load(open('reset_list.p', 'rb'))
        init_data.PASSWORD_RESET = data
    except FileNotFoundError:
        reset_workspace()
        data = init_data.PASSWORD_RESET
        pickle.dump(data, open('reset_list.p', 'wb'))
    try:
        data = pickle.load(open('hangman.p', 'rb'))
        init_data.HANGMAN = data
    except FileNotFoundError:
        reset_workspace()
        data = init_data.HANGMAN
        pickle.dump(data, open('hangman.p', 'wb'))


def save_data():
    '''
    pickle the data into 4 files
    '''
    threading.Timer(2.0, save_data).start()
    # print("Saving data to json file")

    data = init_data.CHANNELS_DICT
    pickle.dump(data, open('channels_dict.p', 'wb'))

    data = init_data.USER_DICT
    pickle.dump(data, open('user_dict.p', 'wb'))

    data = init_data.MESSAGES_DICT
    pickle.dump(data, open('messages_dict.p', 'wb'))

    data = init_data.TOKENS_DICT
    pickle.dump(data, open('tokens_dict.p', 'wb'))

    data = init_data.PASSWORD_RESET
    pickle.dump(data, open('reset_list.p', 'wb'))

    data = init_data.HANGMAN
    pickle.dump(data, open('hangman.p', 'wb'))