import unittest
from unittest.mock import Mock
from data.models import User, UserResponse, TUsername, Role, LoginData, RegisterData, Topic
from routers import users as users_router
from common.responses import NotFound, BadRequest, Unauthorized
from datetime import datetime


mock_user_service = Mock('services.user_service')
mock_topic_service = Mock('services.topic_service')
mock_auth = Mock('common.auth')
users_router.user_service = mock_user_service
users_router.topic_service = mock_topic_service
users_router.get_user_or_raise_401 = mock_auth
datestamp = datetime.now()

def fake_user(id=1, username='username', password='password', first_name='firstname', last_name='lastname', role=Role.ADMIN):
    mock_user = Mock(spec=User)
    mock_user.id = id
    mock_user.username = username
    mock_user.password = password
    mock_user.first_name = first_name
    mock_user.last_name = last_name
    mock_user.role = role
    return mock_user

def fake_user_response(id=1, username='username', fullname='firstname lastname'):
    mock_user_response = Mock(spec=UserResponse)
    mock_user_response.id = id
    mock_user_response.username = username
    mock_user_response.fullname = fullname
    return mock_user_response

def fake_topic(id=1, title='Test_topic', datestamp=datestamp, locked=0, category_id=1, user_id=1):
    mock_topic = Mock(spec=Topic)
    mock_topic.id = id
    mock_topic.title = title
    mock_topic.datestamp = datestamp
    mock_topic.locked = locked
    mock_topic.category_id = category_id
    mock_topic.user_id = user_id
    return mock_topic


class UserRouter_Should(unittest.TestCase):

    def setUp(self):
        mock_user_service.reset_mock()

    def test_login_returns_token_whenUser(self):
        data = LoginData(username='username', password='password')
        user = fake_user()
        token = '1;username'
        mock_user_service.try_login = lambda username, password: user
        mock_user_service.create_token = lambda user: token
        expected = {'token': token}
        result = users_router.login(data=data)

        self.assertEqual(expected, result)

    def test_login_returns_BadRequest_whenNoUser(self):
        data = LoginData(username='username', password='password')
        mock_user_service.try_login = lambda username, password: None

        self.assertEqual(BadRequest, type(users_router.login(data=data)))

    def test_userTopics_returns_listOfTopics_when_TopicsArePresent(self):
        user = fake_user()
        topic1 = fake_topic()
        topic2 = fake_topic(id=2)
        token = '1;username'
        mock_topic_service.get_user_topics = lambda id: [topic1, topic2]

        expected = [topic1, topic2]
        result = users_router.user_topics(token)

        self.assertEqual(expected, result)

    def test_register_returns_UserResponse_when_UsernameIsFree(self):
        data = RegisterData(username='username', password='password', firstname='firstname', lastname='lastname')
        user = fake_user()
        mock_user_service.create = lambda a, b, c, d, e: user
        expected = UserResponse(id=1, username='username', fullname='firstname lastname', role=Role.ADMIN)
        result = users_router.register(data=data)

        self.assertEqual(expected, result)

    def test_register_returns_BadRequest_when_UsernameTaken(self):
        data = RegisterData(username='username', password='password', firstname='firstname', lastname='lastname')
        mock_user_service.create = lambda a, b, c, d, e: None
        
        self.assertEqual(BadRequest, type(users_router.register(data=data)))

