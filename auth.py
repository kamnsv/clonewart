from flask import request, redirect, session
import hashlib
import hmac
import base64
from regist import *
from db import *

def auth(app):  
  
       
    @app.route('/logout')
    def logout():
        session.pop('userId', None)
        session.pop('userSoc', None)
        session.pop('userImg', None)
        session.pop('userName', None)
        return redirect('/')   
    
    def string_generator(data_incoming):
        data = data_incoming.copy()
        del data['hash']
        keys = sorted(data.keys())
        string_arr = []
        for key in keys:
                if data[key] is not None:
                        string_arr.append(key+'='+data[key])
        string_cat = '\n'.join(string_arr)
        return string_cat

    @app.route('/login')
    def login():
        tg_data = {
            "id" :        request.args.get('id',None),
            "first_name": request.args.get('first_name',None),
            "last_name":  request.args.get('last_name', None),
            "username":   request.args.get('username', None),
            "auth_date":  request.args.get('auth_date', None),
            "hash":       request.args.get('hash',None),
            "photo_url":  request.args.get('photo_url',None),
        }

        data_check_string = string_generator(tg_data)
        secret_key = hashlib.sha256(app.config['BOT_TOKEN'].encode('utf-8')).digest()
        secret_key_bytes = secret_key
        data_check_string_bytes = bytes(data_check_string,'utf-8')
        hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
        if hmac_string == tg_data['hash']:
            registration(app, tg_data)
        return redirect('/')