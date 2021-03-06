from sqlalchemy import func, or_, and_, any_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.testing import in_

from end_points.access_layer import _get_session
from models.models import LoginUser, Match

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

def _create_user(data):
    session = _get_session()
    try:
        user = session.query(LoginUser).filter(LoginUser.unique_identifier == data['unique_identifier']).first()
        if user is not None:
            data['login_user_id'] = user.login_user_id
        user = LoginUser(**data)
        session.merge(user)
        try:
            session.commit()
        except IntegrityError as ex:
            if ex.orig.pgcode == '23505':
                return f'User already exists', None
            else:
                return f'Missing required field', None
        return None, None
    finally:
        session.close_all()

def _get_user_other_than_named(current_id):
    try:
        session = _get_session()
        current_user = session.query(LoginUser).filter(LoginUser.unique_identifier == current_id).first()
        if current_user is None:
            return  'No more users', None
        matched_users = session.query(Match).filter(Match.user_1==current_user.login_user_id).all()

        invalid_user_ids = [m.user_2 for m in matched_users]+[current_user.login_user_id]

        user_to_return = session.query(LoginUser).filter(~LoginUser.login_user_id.in_(invalid_user_ids)).order_by(func.random()).first()

        if user_to_return is None:
            return 'No more users', None

        match = Match(user_1=current_user.login_user_id,
                      user_2= user_to_return.login_user_id,
                      status='not_matched')
        session.add(match)
        session.commit()
        user_as_dict = row2dict(user_to_return)
        user_as_dict.pop('login_user_id')
        user_as_dict.pop('unique_identifier')
        return None, user_as_dict
    finally:
        session.close_all()
