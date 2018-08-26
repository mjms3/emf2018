from sqlalchemy.exc import IntegrityError

from end_points.access_layer import _get_session
from lambda_helpers import _success_response, _error_response
from models.models import LoginUser


def create_user(data):
    username = data['username']
    session = _get_session()
    user = LoginUser(username=username)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        return _error_response(f'User: {username} already exists')
    return _success_response()