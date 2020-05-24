''' This file contains the function to upload profile photo '''
import random
import string
from urllib.request import urlopen
from PIL import Image
from user_helper import is_token_valid, get_u_id
from error import AccessError, InputError
import init_data
import os

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a URL of an image on the internet, crops the image
    within bounds (x_start, y_start) and (x_end, y_end).
    Position (0,0) is the top left.
    Input: (token, img_url, x_start, y_start, x_end, y_end)
    Output: {}
    '''
    if not is_token_valid(token):
        raise AccessError(description="Token is not valid")

    try:
        image = Image.open(urlopen(img_url))
    except:
        raise InputError(description="Image is invalid")

    width, height = image.size

    print(image.format)
    if image.format == 'JPG' or image.format == 'JPEG':
        pass
    else:
        raise InputError(description="Image is not a JPG")

    if x_start > width or x_end > width or y_start > height or y_end > height:
        raise InputError(description="Crop dimensions not within image range")

    box = (x_start, y_start, x_end, y_end)
    cropped_image = image.crop(box)

    saving_url = generate_random_url()
    cropped_image.save(saving_url)
    u_id = get_u_id(token)

    init_data.USER_DICT[u_id]['profile_img_url'] = "http://127.0.0.1:8080/get_image/" + saving_url

    return {}

def generate_random_url():
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(12)) + '.jpg'
