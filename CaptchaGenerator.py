from captcha.image import ImageCaptcha;
from flask import session;
import random;
import string;
def get_random_code():
    all_chars = string.ascii_letters + string.digits;
    length=random.randint(3,4);
    random_code = ''.join(random.sample(all_chars,length));
    return random_code;
def create_captcha():
    img=ImageCaptcha();
    #code to genrate random character
    code = get_random_code();
    fcode= get_random_code();
    #storing captcha in session
    session["code"]=code;
    pic_name=fcode+"_captcha.png";
    img.write(code,"static/captcha_file/"+pic_name);
    return pic_name;