#encoding: utf-8

from flask import Flask,session,url_for,redirect
from functools import wraps



#装饰器登陆限制
def login_reguired(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
