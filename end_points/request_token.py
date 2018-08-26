from _md5 import md5
from datetime import datetime, timedelta

from sqlalchemy import desc

from end_points.access_layer import _get_session
from models.models import LoginUser, RequestToken, SubmittedResult


def _generate_token(username):
    SALT = 'ea7c4e8022f1bfb900aaf37f2a68491d'
    return md5(''.join([username, SALT, str(datetime.now())]).encode('ascii')).hexdigest()


def _request_token(username):
    session = _get_session()
    user = session.query(LoginUser).filter_by(username=username).first()
    if user is None:
        return f'Unknown user: {username}', None

    user, request_token, submitted_result = session.query(LoginUser).outerjoin(RequestToken,
                                                                               LoginUser.login_user_id == RequestToken.user_id).outerjoin(
        SubmittedResult, RequestToken.request_token_id == SubmittedResult.request_token_id).filter(
        LoginUser.login_user_id == user.login_user_id).order_by(desc(RequestToken.requested_at)).add_entity(
        RequestToken).add_entity(SubmittedResult).first()

    if request_token is not None and submitted_result is None:
        return 'Latest token has not yet been used', None

    generated_token = _generate_token(username)
    request_token = RequestToken(
        request_token=generated_token,
        user_id=user.login_user_id
    )
    session.add(request_token)
    session.commit()
    return None, generated_token
