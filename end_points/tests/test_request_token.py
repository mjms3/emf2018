from unittest import TestCase
from unittest.mock import patch

from testfixtures import compare, test_datetime

from end_points.access_layer import _get_session
from end_points.request_token import _request_token
from models.models import LoginUser, RequestToken

MODBASE = _request_token.__module__


class TestRequestToken(TestCase):


    def _clear_tables(self):
        self.session.commit()
        self.session.query(RequestToken).delete()
        self.session.query(LoginUser).delete()
        self.session.commit()


    def setUp(self):
        self.session = _get_session()
        self._clear_tables()
        user = LoginUser(username='test_user')
        self.session.add(user)
        self.session.commit()
        self.addCleanup(self._clear_tables)


    def test_request_token(self):
        with patch(MODBASE+'.datetime', test_datetime(2018,1,1,12,0,0)):
            error_message, token = _request_token('test_user')
        compare(expected=None, actual=error_message)
        token = '18b4e0f4c69fca8e117b3091bce5f65e'
        compare(expected=token, actual=token)
        compare(expected=1, actual=len(self.session.query(RequestToken).all()))

    def test_user_does_not_exist(self):
        error_message, token = _request_token('unknown_user')
        compare(expected='Unknown user: unknown_user', actual=error_message)
        compare(expected=None, actual=token)

    def test_request_token_user_has_not_used_previous_token(self):
        _request_token('test_user')
        error_message, token = _request_token('test_user')
        compare(expected='Latest token has not yet been used', actual=error_message)
