from sqlalchemy import func, or_, and_
from sqlalchemy.exc import IntegrityError

from end_points.access_layer import _get_session
from models.models import LoginUser, Match

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
    current_user = session.query(LoginUser).filter(LoginUser.unique_identifier == current_id).first()

    user_to_return = session.query(LoginUser).outerjoin(Match, or_(LoginUser.login_user_id==Match.user_1,
                                                                  LoginUser.login_user_id==Match.user_2)).filter(
        and_(LoginUser.unique_identifier != current_id,
            Match.match_id == None)
    ).order_by(func.random()).first()

    if user_to_return is None:
        return 'No more users', None

    match = Match(user_1=current_user.login_user_id,
                  user_2= user_to_return.login_user_id,
                  status='not_matched')
    session.add(match)
    session.commit()
    user_as_dict = row2dict(user_to_return)
    user_as_dict.pop('login_user_id')
    return None, user_as_dict
