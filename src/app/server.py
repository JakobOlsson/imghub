import logging
from os import getenv
from flask import Flask
from buckethandler.handler import bucket_handler

def config_logging(debug=False):
    print(f"Debug is on?: {debug}")
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

def create_app(debug=False):
    app = Flask(__name__)
    app.register_blueprint(bucket_handler)
    # limit max payload to 50MB
    app.config['MAX_CONTENT_LENGTH']
    config_logging(debug)
    return app

if __name__ == '__main__':
    debug = True if getenv('DEBUG', '').lower() == "true" else False
    app = create_app(debug)
    app.run(debug=debug, host='0.0.0.0')
