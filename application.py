import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from end_points.login_user import _create_user
from end_points.request_token import _request_token
from end_points.response_helpers import _apply_end_point

_log = logging.getLogger('')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
_log.setLevel(logging.DEBUG)
handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=10*1024*1024,backupCount=5)
handler.setFormatter(formatter)

application = Flask(__name__)

@application.route('/create_user/<username>')
def create_user(username):
    return _apply_end_point(_create_user, username)


@application.route('/request_token/<username>')
def generate_token(username):
    return _apply_end_point(_request_token, username)

if __name__ == "__main__":
    application.run()