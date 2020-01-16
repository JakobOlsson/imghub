import logging
from os import getenv
from flask import Flask
from flask_session import Session
from bucket.handler import bucket_handler
from session.handler import session_handler
from werkzeug.middleware.proxy_fix import ProxyFix


def config_logging(debug=False):
    print(f"Debug is on?: {debug}")
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def create_app(debug=False):
    app = Flask(__name__)
    app.register_blueprint(bucket_handler)
    app.config.from_pyfile('settings.py')
    # configure session
    sess = Session()
    sess.init_app(app)
    app.register_blueprint(session_handler)
    # limit max payload to 50MB
    app.config['MAX_CONTENT_LENGTH']
    config_logging(debug)
    return app


def behind_proxy(app):
    # App is behind one proxy that sets the -For and -Host headers.
    app = ProxyFix(app, x_for=1, x_host=1)


if __name__ == '__main__':
    debug = True if getenv('DEBUG', '').lower() == "true" else False
    app = create_app(debug)
    if getenv("PROXIED", "true").lower() == "true":
        behind_proxy(app)

    app.run(debug=debug, host='0.0.0.0')
