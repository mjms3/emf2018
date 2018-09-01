import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request

from end_points.login_user import _create_user
from end_points.response_helpers import _apply_end_point

_log = logging.getLogger('')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
_log.setLevel(logging.DEBUG)
handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=10*1024*1024,backupCount=5)
handler.setFormatter(formatter)

application = Flask(__name__)

@application.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    return _apply_end_point(_create_user, data)

if __name__ == "__main__":
    application.run()