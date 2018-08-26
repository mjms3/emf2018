from sqlalchemy.exc import IntegrityError

from end_points.access_layer import _get_session
from models.models import LoginUser


def _create_user(username):
    session = _get_session()
    user = LoginUser(username=username)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        return f'User: {username} already exists', None
    return None, None