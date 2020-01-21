import logging
from flask import Blueprint
from flask import session
session_handler = Blueprint('session_handler',
                            __name__,
                            template_folder='templates')

LOG = logging.getLogger(__name__)


@session_handler.route('/test/session/get/')
def get_key():
    return session.get('key', 'not set')


@session_handler.route('/test/session/set/')
def set_key():
    session.setdefault('key', default='value is set')
    return 'ok'
