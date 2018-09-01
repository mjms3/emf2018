from unittest import TestCase

from testfixtures import compare

from end_points.access_layer import _get_session
from end_points.login_user import _create_user, _get_user_other_than_named
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
            'unique_identifier': 'FOO',
            'age': '25',
            'tag_line':'my tag line',
            'looking_for' : 'looking_for',
            'contact': 'contact'
        }


    def test_createUser(self):
        self.addCleanup(self._clear_LoginUser_table)

        error_message,result = _create_user(self.user_data)

        compare(expected=(None, None),
                actual=(error_message,result))
        compare(expected=['FOO'],
                actual=[u.unique_identifier for u in self.session.query(LoginUser).all()])

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

        compare(expected=('User already exists', None),
                actual=(error_message,result))

        compare(expected=['FOO'],
                actual=[u.unique_identifier for u in self.session.query(LoginUser).all()])

    def test_getUserToDisplay(self):
        self.addCleanup(self._clear_LoginUser_table)

        _,_ = _create_user(self.user_data)
        current_user = self.user_data['unique_identifier']
        self.user_data['unique_identifier'] = 'BAR'

        _, _ = _create_user(self.user_data)

        error_message, result = _get_user_other_than_named(current_user)

        for f in ('humidity','magnetic_flux','temperature'):
            self.user_data[f] = 'None'
        compare(expected=(None, self.user_data),
                actual=(error_message,result))
