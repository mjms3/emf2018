import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from end_points.response_helpers import _success_response, _error_response
from end_points.login_user import _create_user

_log = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
_log.setLevel(logging.DEBUG)
handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=10*1024*1024,backupCount=5)
handler.setFormatter(formatter)

application = Flask(__name__)

@application.route('/create_user/<username>')
def create_user(username):
    try:
        error_message = _create_user(username)
        if error_message is None:
            return _success_response()
        elif isinstance(error_message,str):
            return _error_response(error_message)
        else:
            raise ValueError(f'Unexpected return value: {error_message}')
    except Exception:
        _log.exception("Failed to create user:\n")

if __name__ == "__main__":
    application.run()