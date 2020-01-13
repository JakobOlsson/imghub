import logging
from os import getenv
from flask import Blueprint, render_template
from flask import request, redirect, jsonify, session
session_handler = Blueprint('session_handler', __name__, template_folder='templates')

LOG = logging.getLogger(__name__)

@session_handler.route('/login')
def login_page():
    return render_template('login.html')

@session_handler.route('/get/')
def get_key():
    return session.get('key', 'not set')

@session_handler.route('/set/')
def set_key():
    session.setdefault('key', default='value is set')
    return 'ok'
