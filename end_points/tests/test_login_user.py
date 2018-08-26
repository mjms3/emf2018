from unittest import TestCase

from testfixtures import compare

from end_points.access_layer import _get_session
from end_points.login_user import _create_user
from models.models import LoginUser


class TestLoginUser(TestCase):

    def _clearLoginUserTable(self):
        self.session.query(LoginUser).delete()
        self.session.commit()

    def setUp(self):
        self.session = _get_session()

    def test_createUser(self):
        self.addCleanup(self._clearLoginUserTable)
        error_message = _create_user('my_user_name')

        compare(expected=None, actual=error_message)
        compare(expected=['my_user_name'],
                actual=[u.username for u in self.session.query(LoginUser).all()])

    def test_createUser_whenUserAlreadyExists(self):
        self.addCleanup(self._clearLoginUserTable)

        for _ in range(2):
            error_message = _create_user('my_user_name')

        compare(expected='User: my_user_name already exists', actual=error_message)

        compare(expected=['my_user_name'],
                actual=[u.username for u in self.session.query(LoginUser).all()])

