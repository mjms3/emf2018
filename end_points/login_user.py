from sqlalchemy.exc import IntegrityError

from end_points.access_layer import _get_session
from models.models import LoginUser


row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

def _create_user(data):
    session = _get_session()
    user = LoginUser(**data)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as ex:
        if ex.orig.pgcode == '23505':
            return f'User already exists', None
        else:
            return f'Missing required field', None
    return None, None

def _get_user_other_than_named(current_id):
    session = _get_session()
    user_to_return = session.query(LoginUser).filter(LoginUser.unique_identifier != current_id).first()
    user_as_dict = row2dict(user_to_return)
    user_as_dict.pop('login_user_id')
    return None, user_as_dict
