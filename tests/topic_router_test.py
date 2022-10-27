import unittest
from unittest.mock import Mock
from data.models import Category, Reply, Topic, TopicResponse, User, Role, UserResponse
from routers import topics as topics_router
from datetime import datetime
from common.responses import NotFound, BadRequest, Unauthorized

mock_topic_service = Mock(spec='services.topic_service')
mock_category_service = Mock(spec='services.category_service')
mock_user_service = Mock(spec='services.user_service')

topics_router.topic_service = mock_topic_service
topics_router.category_service = mock_category_service
topics_router.user_service = mock_user_service
datestamp = datetime.now()

def fake_category(id=1, name='Test_category', locked=False):
    mock_category = Mock(spec=Category)
    mock_category.id = id
    mock_category.name = name
    mock_category.locked = locked
    return mock_category

def fake_user(id=1, username='pesho', password='pesho', firstname='pesho', lastname='pesho', role=Role.ADMIN):
    mock_user = Mock(spec=User)
    mock_user.id = id
    mock_user.username = username
    mock_user.password = password
    mock_user.first_name = firstname
    mock_user.last_name = lastname
    mock_user.role = role
    return mock_user

def fake_topic(id=1, title='Test_topic', datestamp=datestamp, locked=0, category_id=1, user_id=1):
    mock_topic = Mock(spec=Topic)
    mock_topic.id = id
    mock_topic.title = title
    mock_topic.datestamp = datestamp
    mock_topic.locked = locked
    mock_topic.category_id = category_id
    mock_topic.user_id = user_id
    return mock_topic


class TopicRouter_Should(unittest.TestCase):

    def setUp(self):
        mock_category_service.reset_mock()
        mock_topic_service.reset_mock()
        mock_user_service.reset_mock()

    def test_getTopics_returns_emptyList_when_noTopics(self):
        mock_topic_service.all = lambda key, search: []
        self.assertEqual([], topics_router.get_topics())

    def test_getTopics_returns_listOfTopics_whenThereAreTopics(self):
        topic1 = fake_topic()
        topic2 = fake_topic(id=2)
        mock_topic_service.all = lambda key, search: [topic1, topic2]

        self.assertEqual([topic1, topic2], topics_router.get_topics())

    def test_getTopicById_returns_NotFound_when_noTopic(self):
        mock_topic_service.get_by_id = lambda id: None
        result = topics_router.get_topic_by_id(1)
        expected = NotFound

        self.assertEqual(expected, type(result))

    def test_getTopicById_returns_Topic_when_ThereIsATopic(self):
        topic1 = fake_topic()
        category1 = fake_category()
        user1 = fake_user()
        mock_topic_service.get_by_id = lambda id: topic1
        mock_topic_service.get_topic_replies = lambda id: []
        mock_category_service.get_by_id = lambda id: category1
        mock_user_service.find_by_id = lambda id: user1

        replies = []
        user_response = UserResponse(id=user1.id, username=user1.username, fullname=(f'{user1.first_name} {user1.last_name}'), role=user1.role)
        expected = TopicResponse(id=topic1.id, author=user_response, title=topic1.title, category=category1, datestamp=datestamp, replies=replies, locked=False)
        result = topics_router.get_topic_by_id(1)

        self.assertEqual(expected, result)

    # def test_createTopic_createsTopic(self):
    #     topic1 = fake_topic()
    #     category1 = fake_category()
    #     mock_category_service.get_by_id = lambda id: category1
    #     mock_topic_service.create = lambda topic: topic1
    #     token = '1;pesho'

    #     self.assertEqual(topic1, topics_router.create_topic(topic1))

    # def test_createTopic_returns_BadRequest_ifCategoryIsLocked(self):
    #     topic1 = fake_topic()
    #     category1 = fake_category(locked=True)
    #     mock_category_service.get_by_id = lambda id: category1
    #     mock_topic_service.create = lambda topic: topic1

    #     self.assertEqual(BadRequest, type(topics_router.create_topic(topic1)))

    # def test_updateTopic_updates_theTopic(self):
    #     old_topic = fake_topic()
    #     new_topic = fake_topic(title='New_Test_Topic', locked=1, category_id=2)
    #     old_topic_id = old_topic.id
    #     merged_topic = fake_topic(
    #         id=old_topic.id, title=new_topic.title, datestamp=old_topic.datestamp,
    #         locked=new_topic.locked, category_id=new_topic.category_id, user_id=old_topic.user_id)
    #     user = fake_user()
    #     user.is_admin.return_value = True
    #     token = '1;pesho'
    #     mock_user_service.is_authenticated = lambda token: user
    #     mock_topic_service.update = lambda old_topic, new_topic: merged_topic
    #     mock_topic_service.get_by_id = lambda old_topic_id: old_topic

    #     self.assertEqual(merged_topic, topics_router.update_topic(old_topic_id, new_topic, token))

    # def test_updateTopic_returns_Unauthorized_whenUserDoesntOwnTheTopic(self):
    #     old_topic = fake_topic(user_id=2)
    #     new_topic = fake_topic(title='New_Test_Topic', locked=1, category_id=2)
    #     old_topic_id = old_topic.id
    #     user = fake_user()
    #     token = '1;pesho'
    #     mock_user_service.is_authenticated = lambda token: user
    #     mock_topic_service.get_by_id = lambda old_topic_id: old_topic

    #     self.assertEqual(Unauthorized, type(topics_router.update_topic(old_topic_id, new_topic, token)))

    # def test_updateTopic_returns_NotFound_whenNoTopic(self):
    #     topic1 = fake_topic()
    #     user = fake_user()
    #     token = '1;pesho'
    #     topic_id = 2

    #     mock_user_service.is_authenticated = lambda token: user
    #     mock_topic_service.get_by_id = lambda id: None

    #     self.assertEqual(NotFound, type(topics_router.update_topic(topic_id, topic1, token)))

    # def test_lockUnlockTopic_locks_Topic(self):
    #     topic1 = fake_topic()
    #     user = fake_user()
    #     token = '1;pesho'
        

    #     mock_user_service.is_authenticated = lambda token: user
    #     mock_topic_service.get_by_id = lambda id: topic1
    #     mock_topic_service.lock_unlock = lambda id: topic1
    #     self.assertEqual(topic1.locked, 0)
    #     result = topics_router.lock_unlock_topic(1, token)
    #     self.assertEqual(topic1, result)
    #     self.assertEqual(topic1.locked, result.locked)

    # def test_lockUnlockTopic_returns_Unauthorized_ifUserNotAdmin(self):
    #     topic1 = fake_topic()
    #     user = fake_user(role=Role.USER)
    #     token = '1;pesho'
        

    #     mock_user_service.is_authenticated = lambda token: user
    #     mock_topic_service.get_by_id = lambda id: topic1
    #     mock_topic_service.lock_unlock = lambda id: topic1

    #     self.assertEqual(topic1.locked, 0)
    #     result = topics_router.lock_unlock_topic(1, token)
    #     self.assertEqual(Unauthorized, type(result))
