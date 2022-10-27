import unittest
from data.models import User, UserResponse, Role
from services import user_service
from mariadb import IntegrityError

class UserService_Should(unittest.TestCase):

    def test_findByUser_returns_User_whenThereIsOne(self):
        get_data_func = lambda q, username: [(1, 'username', 'password', 'firstname', 'lastname', Role.USER)]

        expected = User(id=1, username='username', password='password', first_name='firstname', last_name='lastname', role=Role.USER)
        result = user_service.find_by_username(username='username', get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_findByUser_returns_None_whenNoUser(self):
        get_data_func = lambda q, username: []
        
        self.assertEqual(None, user_service.find_by_username(username='username', get_data_func=get_data_func))

    def test_findById_returns_User_whenThereIsOne(self):
        get_data_func = lambda q, id: [(1, 'username', 'password', 'firstname', 'lastname', Role.USER)]

        expected = User(id=1, username='username', password='password', first_name='firstname', last_name='lastname', role=Role.USER)
        result = user_service.find_by_id(id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_findById_returns_None_whenNoUser(self):
        get_data_func = lambda q, id: []

        self.assertEqual(None, user_service.find_by_id(id=1, get_data_func=get_data_func))

    def test_create_returns_User_when_noError(self):
        insert_data_func = lambda q, a: 1

        expected = User(id=1, username='username', password='', first_name='firstname', last_name='lastname', role=Role.USER)
        result = user_service.create(username='username', password='password', firstname='firstname', lastname='lastname', role=Role.USER, insert_data_func=insert_data_func)

        self.assertEqual(expected, result)

    def test_create_returns_None_whenError(self):
        def insert_data_func(q, a):
            raise IntegrityError

        expected = None
        result = user_service.create(username='username', password='password', firstname='firstname', lastname='lastname', role=Role.USER, insert_data_func=insert_data_func)

        self.assertEqual(expected, result)

    def test_promoteDemote_promotes_User(self):
        update_data_func = lambda q, user: None

        user = User(id=1, username='username', password='', first_name='firstname', last_name='lastname', role=Role.USER)
        expected = User(id=1, username='username', password='', first_name='firstname', last_name='lastname', role=Role.ADMIN)
        result = user_service.promote_demote(user=user, update_data_func=update_data_func)

        self.assertEqual(expected, result)

    def test_createToken_creates_Token(self):
        user = User(id=1, username='username', password='', first_name='firstname', last_name='lastname', role=Role.USER)

        expected = '1;username'
        result = user_service.create_token(user=user)

        self.assertEqual(expected, result)

