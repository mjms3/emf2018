from sqlalchemy.exc import IntegrityError

from end_points.access_layer import _get_session
from models.models import LoginUser


def _create_user(data):
    session = _get_session()
    user = LoginUser(**data)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as ex:
        if ex.orig.pgcode == '23505':
            return f'User: {data["username"]} already exists', None
        else:
            return f'Missing required field', None
    return None, None