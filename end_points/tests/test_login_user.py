from unittest import TestCase

from testfixtures import compare

from end_points.access_layer import _get_session
from end_points.login_user import _create_user
from models.models import LoginUser


class TestLoginUser(TestCase):

    def _clear_LoginUser_table(self):
        self.session.query(LoginUser).delete()
        self.session.commit()

    def setUp(self):
        self.session = _get_session()
        self._clear_LoginUser_table()
        self.user_data  = {
            'username': 'my_user_name',
            'age': 25,
            'tag_line':'my tag line',
            'looking_for' : 'looking_for',
            'contact': 'contact'
        }


    def test_createUser(self):
        self.addCleanup(self._clear_LoginUser_table)

        error_message,result = _create_user(self.user_data)

        compare(expected=(None, None),
                actual=(error_message,result))
        compare(expected=['my_user_name'],
                actual=[u.username for u in self.session.query(LoginUser).all()])

    def test_createUser_whenMissingData(self):
        self.addCleanup(self._clear_LoginUser_table)
        self.user_data.pop('tag_line')
        error_message, result = _create_user(self.user_data)

        compare(expected=("Missing required field", None),
                actual=(error_message,result))

    def test_createUser_whenUserAlreadyExists(self):
        self.addCleanup(self._clear_LoginUser_table)

        for _ in range(2):
            error_message, result = _create_user(self.user_data)

        compare(expected=('User: my_user_name already exists', None),
                actual=(error_message,result))

        compare(expected=['my_user_name'],
                actual=[u.username for u in self.session.query(LoginUser).all()])

