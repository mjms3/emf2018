import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request

from end_points.login_user import _create_user, _get_user_other_than_named, _mark_as_matched
from end_points.response_helpers import _apply_end_point

_log = logging.getLogger('')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
_log.setLevel(logging.DEBUG)
handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=10*1024*1024,backupCount=5)
handler.setFormatter(formatter)

application = Flask(__name__)

@application.route('/create_user', methods=['POST'])
def create_user():
    _log.info('Request: %s\n%s', request, request.__dict__)
    data = request.json
    return _apply_end_point(_create_user, data)

@application.route('/get_user/<user_identifier>', methods=['GET'])
def get_user(user_identifier):
    return _apply_end_point(_get_user_other_than_named, user_identifier)

@application.route('/matched/<current_user>/<matched_user>')
def matched(current_user, matched_user):
    return _apply_end_point(_mark_as_matched, (current_user,matched_user))

if __name__ == "__main__":
    application.run()