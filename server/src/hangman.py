import init_data
from channel import channel_invite
import random
import uuid
import time
import threading
from error import InputError, AccessError

def generate_a_word():
    ''' Generates a random guessing word
    '''
    words = open("words.txt").readlines() 
    i = random.randint(0,853)
    words = words[i]
    words = words.split()
    words = words[0]
    return words

def check_guess(message):
    ''' Checks that message sent by user is '/guess'
        Input: message
        Output: 0, 1
    '''
    string = '/guess '
    
    if len(message) <= len(string):
        return 0
        
    i = 0
    while i < len(string):
        if message[i] != string[i]:
            return 0
        i += 1
        
    return 1

# active when user send message '/hangman'
# set game up for current channel
def hangman_start(channel_id, token):
    ''' 
    Starts hangman game in channel_id
    Input: channel_id, token
    Output: {}
    ''' 
    if init_data.HANGMAN == {}:   
        robot = auth_register('hangman@gmail.com', 'hangmanrobot', 'hangman', 'robot')
        
        init_data.USER_DICT['robot_u_id'] = init_data.USER_DICT.pop(robot['u_id'])
        
        init_data.TOKENS_DICT["valid_tokens"]['robot_token'] = init_data.TOKENS_DICT["valid_tokens"].pop(robot['token'])
        
        init_data.TOKENS_DICT["valid_tokens"]['robot_token'] = 'robot_u_id'
    

    # Invite hangman robot into current channel
    channel_invite(token, channel_id, 'robot_u_id')    
    
    # Add channel_id into hangman data store
    i = 0
    for key in init_data.HANGMAN:
        if key == 'c_id':
            i = 1
        # game already started
        if key == channel_id:
            i = 2
    if i == 1:
        init_data.HANGMAN[channel_id] = init_data.HANGMAN.pop('c_id')
    
    # Hangman game has started in slackr 
    elif i == 2:
        send_type = '1: Hangman has already started in channel'
    # Start hangman game in channe
    else:
        send_type = '2: Start hangman game'
        init_data.HANGMAN[channel_id] = {
            'word': '',
            'word_template': '',
            'hangman': '',
            'letter_guessed': '',
            'letter_found': '',
            'num_letters_to_guess': '',
            'num_wrong_guesses': ''
        }
        # Obtain new word store in data store as upper case
        new_word = generate_a_word().upper()
        init_data.HANGMAN[channel_id]['word'] = new_word
        # Set word template 
        init_data.HANGMAN[channel_id]['word_template'] = word_template(new_word)
        # Set number of letters users need to guess right
        init_data.HANGMAN[channel_id]['num_letters_to_guess'] = num_letters_in_word(new_word)
        
    hangman_reply(send_type, channel_id)
    
    return {}

def hangman_reply(send_type, c_id):
    ''' Hangman bot replies in channel when /hangman is sent
        Input: send_type, c_id
        Output: {}
    '''
    # Check type of hangman case
    case = int(send_type[0])

    # Case 1: Hangman has already started in channel
    if case == 1:
        msg_1 = 'A hangman game has already started in this channel \n'
        msg_2 = 'Message /guess - to end the last game and then'
        msg_3 = '/hangman to start a new game\n'
        message = msg_1 + msg_2 + msg_3
    # Case 2: Start hangman game
    else:
        msg_1 = "Welcome to Hangman game! \n"
        msg_2 = "To win the game, you need to guess the correct word.\n\n"
        msg_3 = "You can choose guess either a letter or a word\n"
        msg_4 = "Type in '/guess X' where X is any letter, to guess a single letter.\n"
        msg_5 = "OR Type in '/guess XXX' where XXX is any word you are guess, to guess the word.\n"
        msg_6 = "Note: u have to type in '/guess ' in lowercase\n\n"
        msg_7 = "You can choose to give up the game by type in '/guess -'.\n"
        msg_8 = "you have 13 chance in total to guess the wrong letter or word\n"
        msg_9 = "Once the hangman is drawn, you lose the game.\n"
        msg_10 = "The dead hangman looks like this: \n" + hangman_draw('instruction', c_id)
        msg_11 = "Good Luck!\n"
        message = msg_1 + msg_2 + msg_3 + msg_4 + msg_5 + msg_6 + msg_7 + msg_8 + msg_9 + msg_10 + msg_11

    hangman_send('robot_token', c_id, message)

    return {}

def num_letters_in_word(word):
    ''' Calculate the number of letters that users need to guess in word
        Input: word
        Output: num_letters
    ''' 
    letters = []
    for key in word:
        if key not in letters:
            letters.append(key)
    num_letters = len(letters)
    return num_letters

def check_input_letter(letter, c_id):
    ''' Checks the input /guess X
        Input: letter, c_id
        Output: boolean
    ''' 
    # User wants to terminate hangman game
    if letter == '-':
        return 2
    
    # User guessed a letter that was already guessed
    for key in init_data.HANGMAN[c_id]['letter_guessed']:
        if key == letter:
            # CHANGE THIS
            print("letter " + letter + " already been guessed")
            return 0
    init_data.HANGMAN[c_id]['letter_guessed'] += letter
    
    # User guessed a letter
    for key in init_data.HANGMAN[c_id]['word']:
        if key == letter:
            # Length of string letter_found is one character longer if user guessed correct letter
            init_data.HANGMAN[c_id]['letter_found'] += letter

    return 1

def hangman_check(c_id, u_id, message):
    ''' Checks if user correctly guesses a letter or the whole word
        Input: c_id, u_id, message
        Output: {}
    '''

    # Convert all guess letter or guess word to upper case
    input_message = message
    message = '/guess '
    
    i = 7
    while i < len(input_message):
        message += input_message[i].upper()
        i += 1
    i = 7
    
    # User guesses a letter
    num_letter_found_b4_check = len(init_data.HANGMAN[c_id]['letter_found'])
    if len(message) == 8:
        boolean = check_input_letter(message[8], c_id)
        # User tries to guess a letter
        if boolean == 1:
            # Word  DOES contain current letter
            num_letter_found_afr_check = len(init_data.HANGMAN[c_id]['letter_found'])
            if num_letter_found_b4_check != num_letter_found_afr_check:
                letter = message[7]
                # Update word_template
                hangman_word(c_id, letter)
                # User wins hangman game
                if num_letter_found_afr_check == init_data.HANGMAN[c_id]['num_letters_to_guess']:
                    send_type = '1: User guessed final letter and wins game'
                else:
                    send_type = '2: User guessed correct letter'
            # Word DOES NOT contain letter
            else:
                # Update number of wrong guesses made
                init_data.HANGMAN[c_id]['num_wrong_guesses'] += 1
                # Update hangman drawing in datastore
                init_data.HANGMAN[c_id]['hangman'] = hangman_draw('hangman_draw', c_id)
                if init_data.HANGMAN[c_id]['num_wrong_guesses'] == 13:
                    send_type = '3: Game lost'
                else:
                    send_type = '4: User guessed incorrect letter'
        # User chooses to terminate game
        elif boolean == 2:
            reset_hangman(c_id)
            send_type = '5: Game terminated'
            return {}
        # Letter already been guessed  
        else:
            send_type = '6: Letter already guessed'
            return {}
        
    # User tries to guess whole word
    else:
        # Create word being guessed from message sent
        word_guess = ''
        while i < len(message):
            word_guess += message[i] 
            i += 1
        # User guessed correct word
        if check_word_guess(word_guess, c_id):
            send_type = '7: User guessed correct word'
            reset_hangman(c_id)
            return {}
        # User DID NOT guess correct word
        else:
            init_data.HANGMAN[c_id]['num_wrong_guesses'] += 1
            send_type = '8: User guessed incorrect word'
            # CHANGE THIS
            hangman_draw('hangman_draw', c_id)

    guess_reply(send_type, c_id, u_id)

    return {}

def guess_reply(send_type, c_id, u_id):
    ''' Hangman bot replied in channel when /guess X is sent
        Input: send_type, c_id, u_id
        Output: {}
    '''
    # Check type of hangman case
    case = int(send_type[0])

    # Obtain users first name
    name = init_data.USER_DICT[u_id]['name_first']
    
    # Case 1: User guessed final letter and wins game
    if case == 1:
        msg_1 = init_data.HANGMAN[c_id]['word_template'] + '\n'
        msg_2 = init_data.HANGMAN[c_id]['hangman'] 
        msg_3 = 'Letters already guessed: ' + init_data.HANGMAN[c_id]['letter_guessed'] + '\n'
        msg_4 = name + 'has won the game! \n'
        message = msg_1 + msg_2 + msg_3 + msg_4
    # Case 2: User guessed correct letter
    elif case == 2:
        msg_1 = init_data.HANGMAN[c_id]['word_template'] + '\n'
        msg_2 = init_data.HANGMAN[c_id]['hangman']
        msg_3 = 'Letters already guessed: ' + init_data.HANGMAN[c_id]['letter_guessed'] + '\n'
        msg_4 = name + 'has guessed a correct letter \n'
        message = msg_1 + msg_2 + msg_3 + msg_4
    # Case 3: Game lost
    elif case == 3:
        msg_1 = init_data.HANGMAN[c_id]['word_template'] + '\n'
        msg_2 = init_data.HANGMAN[c_id]['hangman']
        msg_3 = 'Letters already guessed: ' + init_data.HANGMAN[c_id]['letter_guessed'] + '\n'
        msg_4 = 'The hangman is dead.\n GAME OVER :(\n'
        message = msg_1 + msg_2 + msg_3 + msg_4
    # Case 4: User guessed incorrect letter
    elif case == 4:
        msg_1 = init_data.HANGMAN[c_id]['word_template'] + '\n'
        msg_2 = init_data.HANGMAN[c_id]['hangman']
        msg_3 = 'Letters already guessed: ' + init_data.HANGMAN[c_id]['letter_guessed'] + '\n'
        msg_4 = 'Oh no the hangman is dying!' + name + 'that was NOT the correct letter\n'
        message = msg_1 + msg_2 + msg_3 + msg_4
    # Case 5: Game terminated
    elif case == 5:
        message = 'Hangman game ended \n The word was ' + init_data.HANGMAN[c_id]['word'] 
    # Case 6: Letter already guessed
    elif case == 6:
        msg_1 = init_data.HANGMAN[c_id]['word_template'] + '\n'
        msg_2 = init_data.HANGMAN[c_id]['hangman']
        msg_3 = 'Letters already guessed: ' + init_data.HANGMAN[c_id]['letter_guessed'] + '\n'
        msg_4 = name + 'That letter has already been guessed\n'
        message = msg_1 + msg_2 + msg_3 + msg_4
    # Case 7: User guessed correct word
    elif case == 7:
        msg_1 = init_data.HANGMAN[c_id]['hangman']
        msg_2 = 'Letters already guessed: ' + init_data.HANGMAN[c_id]['letter_guessed'] + '\n'
        msg_3 = name + 'guessed the word!' + name + 'wins and hangman is saved! :D'
        msg_4 = 'The word was ' + init_data.HANGMAN[c_id]['word'] 
        message = msg_1 + msg_2 + msg_3 + msg_4
    # Case 8: User guessed incorrect word
    else:
        msg_1 = init_data.HANGMAN[c_id]['word_template'] + '\n'
        msg_2 = init_data.HANGMAN[c_id]['hangman']
        msg_3 = 'Letters already guessed: ' + init_data.HANGMAN[c_id]['letter_guessed'] + '\n'
        msg_4 = 'Oh no the hangman is dying!' + name + ', sorry that was not the correct word :(\n'
        message = msg_1 + msg_2 + msg_3 + msg_4

    message_send('robot_token', c_id, message)

    return {}

def reset_hangman(c_id):
    ''' Reset hangman for current channel
        Input: c_id
        Output: {} '''
    del init_data.HANGMAN['c_id']
    
    if init_data.HANGMAN == {}:
        init_data.HANGMAN['c_id'] = {
            'word' : '',
            'word_template': '',
            'hangman': '',
            'letter_guessed' : '',
            'letter_found' : '',
            'num_wrong_guesses': ''
        }
    
    return {}

# check word guessed by user is true or not
def check_word_guess(word_guess, c_id):
    ''' Checks if user guessed correct word
        Input: word_guess, c_id
        Output: 0, 1
    '''
    if len(word_guess) != len(init_data.HANGMAN[c_id]['word']):
        return 0
    
    i = 0
    while i < len(word_guess):
        if word_guess[i] != init_data.HANGMAN[c_id]['word']:
            return 0
        i += 1
        
    return 1

# This function will be called in hangman_start
def word_template(c_id):
    ''' Creates template for word
        Input: c_id
        Output: word_template
    '''
    # Obtain word from dictionary
    word = init_data.HANGMAN[c_id]['word']

    # Create word template "_ _ _ _" for hangman word
    length = len(word) - 1
    i = 0
    word_template = ""
    while i < length:
        word_template = word_template + "_ "
        i += 1
    word_template = word_template + "_"
    
    return word_template

def hangman_word(c_id, letter):
    ''' Updates word_template with correctly guessed letter
        Input: c_id, letter
        Output: {}
    '''
    # Obtain word and current word template
    word = init_data.HANGMAN[c_id]['word']
    word_template = init_data.HANGMAN[c_id]['word_template']
    
    # Store locations where letter occurs in the word into a list
    location_index = []
    i = 0
    length = len(word)
    while i < length:
        if word[i] == letter:
            location_index.append(i)
        i += 1
    
    # Fill in word_template with letter at location
    word_list = list(word_template)
    for key in location_index:
        if key != 0:
            i = key * 2
        else:
            i = 0
        del word_list[i]
        word_list.insert(i, letter)
    blank = ""
    word_template = blank.join(word_list)

    # Update word_template in data store
    init_data.HANGMAN[c_id]['word_template'] = word_template

    # ADD
    # Will send the word as well

def hangman_draw(function, c_id):
    ''' Draws the hangman for number of wrong guesses made OR for demonstration in hangman_help
        Input: num_wrong_guesses
        Outut: {}
    '''
    # Check function condition
    # Used whenever user sends '/guess X'
    if function == 'hangman_draw':
        num_wrong_guesses = init_data.HANGMAN[c_id]['num_wrong_guesses']
    # Used in hangman_start and hangman_help to demonstrate hamgman drawing
    elif function == 'instruction':
        num_wrong_guesses = 14 

    # Maximum number of wrong guesses until hangman dies is 13
    if num_wrong_guesses == 0:
        hangman = "Hangman is unscathed, alive and thriving!"
    elif num_wrong_guesses == 1:
        message = "HANGMAN DRAWING \n\n\n\n\n\n\n\n\n"
        str_2 = " _________     \n"
        hangman = message + str_2
    elif num_wrong_guesses == 2:
        message = "HANGMAN DRAWING \n\n\n\n\n\n\n\n"
        str_1 = " _________     \n"
        str_2 = " _________     \n"
        hangman = message + str_1 + str_2
    elif num_wrong_guesses == 3:
        message = "HANGMAN DRAWING \n\n\n\n\n\n\n\n"
        str_1 = " _________     \n"
        str_2 = " _________|    \n"
        hangman = message + str_1 + str_2
    elif num_wrong_guesses == 4:
        message = "HANGMAN DRAWING \n\n\n\n\n\n\n\n"
        str_1 = " _________     \n"
        str_2 = "|_________|    \n"
        hangman = message + str_1 + str_2
    elif num_wrong_guesses == 5:
        message = "HANGMAN DRAWING \n\n"
        str_2 = "|        \n"
        str_3 = "|        \n"
        str_4 = "|        \n"
        str_5 = "|        \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 6:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|        \n"
        str_3 = "|        \n"
        str_4 = "|        \n"
        str_5 = "|        \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 7:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|         |    \n"
        str_3 = "|        \n"
        str_4 = "|        \n"
        str_5 = "|        \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 8:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|         |    \n"
        str_3 = "|         0    \n"
        str_4 = "|         \n"
        str_5 = "|        \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 9:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|         |    \n"
        str_3 = "|         0    \n"
        str_4 = "|         | \n"
        str_5 = "|        \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 10:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|         |    \n"
        str_3 = "|         0    \n"
        str_4 = "|        /|\n"
        str_5 = "|        \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 11:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|         |    \n"
        str_3 = "|         0    \n"
        str_4 = "|        /|\  \n"
        str_5 = "|         \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 12:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|         |    \n"
        str_3 = "|         0    \n"
        str_4 = "|        /|\\  \n"
        str_5 = "|        / \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9
    elif num_wrong_guesses == 13 or num_wrong_guesses == 14:
        message = "HANGMAN DRAWING \n"
        str_1 = " _________     \n"
        str_2 = "|         |    \n"
        str_3 = "|         0    \n"
        str_4 = "|        /|\\  \n"
        str_5 = "|        / \\  \n"
        str_6 = "|              \n"
        str_7 = "|              \n"
        str_8 = "|_________     \n"
        str_9 = "|_________|    \n"
        hangman = message + str_1 + str_2 + str_3 + str_4 + str_5 + str_6 + str_7 + str_8 + str_9

    return hangman

def hangman_send(token, channel_id, message):
    
    '''
    Sends a message in a channel
    Input: (token, channel_id, message)
    Output: { message_id }
    '''

    u_id = get_u_id(token)

    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")

    if not is_user_in_channel(u_id, channel_id):
        raise AccessError(description="You are not a member of channel")

    message_id = generate_message_id(channel_id)
    time_created = int(time.time())

    new_message = {}

    new_message["message_id"] = message_id
    new_message["u_id"] = u_id
    new_message["message"] = message
    new_message["time_created"] = time_created
    new_message["is_pinned"] = False
    new_message["react"] = ""
    
    # pull out all c_ids in message_dict
    message_dict = init_data.MESSAGES_DICT
    c_ids = [c_id for c_id in message_dict]

    # check if message_dict already contains a list of messages
    if channel_id in c_ids:
        init_data.MESSAGES_DICT[channel_id].insert(0,new_message)
    # if message is the first one in the channel_id make a new list and insert message in list 
    else:
        init_data.MESSAGES_DICT[channel_id] = []
        init_data.MESSAGES_DICT[channel_id].insert(0,new_message)

    return {'message_id': message_id}

    def generate_message_id(c_id):
        return len(init_data.MESSAGES_DICT[c_id]) + 1
