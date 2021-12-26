from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_shop.modles import User
from utils.messages import to_dict_msg
import functools

def generate_auth_token(uid, expiration):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': uid}).decode()

def verify_auth_token(token_str):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token_str)
    except Exception:
        return None
    usr = User.query.filter_by(id = data['id']).first()
    return usr

def login_required(view_func):
    functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            token = request.headers.get('token')
        except Exception:
            return to_dict_msg(10016)
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return to_dict_msg(10017)
        return view_func(*args, **kwargs)
    return verify_token
