from http import HTTPStatus
from unittest import TestCase

from testfixtures import compare

from end_points.access_layer import _get_session
from end_points.user import create_user
from models.models import LoginUser


class TestUser(TestCase):

    def _clearUserTable(self):
        self.session.query(LoginUser).delete()
        self.session.commit()

    def setUp(self):
        self.session = _get_session()

    def test_createUser(self):
        self.addCleanup(self._clearUserTable)
        response = create_user({
            'username': 'my_user_name'
        })

        compare(expected={
            'headers': {
                'Content-Type': 'application/json'
            },
            'statusCode': HTTPStatus.OK},
            actual=response)

        compare(expected=['my_user_name'],
                actual=[u.username for u in self.session.query(LoginUser).all()])

    def test_createUser_whenUserAlreadyExists(self):
        self.addCleanup(self._clearUserTable)

        for _ in range(2):
            response = create_user({
                'username': 'my_user_name'
            })

        compare(expected={
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': '{"error": "User: my_user_name already exists"}',
            'statusCode': HTTPStatus.BAD_REQUEST},
            actual=response)

        compare(expected=['my_user_name'],
                actual=[u.username for u in self.session.query(LoginUser).all()])