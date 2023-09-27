import os
import secrets
from PIL  import Image
from flask import  url_for,current_app
from flaskblog import  mail
from flask_mail import Message 

def save_picture(formpicture):
    random_hex = secrets.token_hex(8)
    _, f_ext =  os.path.splitext(formpicture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)
    image_size = (125,125)
    i = Image.open(formpicture)
    i.thumbnail(image_size)
    i.save(picture_path)
    # formpicture.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="chordograph@gmail.com",recipients=[user.email])
    msg.body =f'''
                To reset your password, visit the following link:
                    <a href="{url_for('users.reset_token',token=token,_enternal=True)}"> click here </a>

                If you did not make this request then simply ignore this email and no changes will be made
                '''
    mail.send(msg)
