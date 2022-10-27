import unittest
from data.models import Topic
from services import topic_service
from datetime import datetime
from common.responses import NotFound

datestamp = datetime.now()
class TopicService_Should(unittest.TestCase):

    def test_all_creates_ListOfTopics_when_DataIsPresent(self):
        get_data_func = lambda q: [(1, 'Title1', datestamp, 1, 1, 1), (2, 'Title2', datestamp, 1, 1, 1)]
        expected = [Topic(id=1, title='Title1', datestamp=datestamp, locked=1, category_id=1, user_id=1),
        Topic(id=2, title='Title2', datestamp=datestamp, locked=1, category_id=1, user_id=1)]
        result = list(topic_service.all(get_data_func=get_data_func))

        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(expected, result)
        self.assertEqual(2, len(result))

    def test_all_creates_EmptyList_when_NoData(self):
        get_data_func = lambda q: []
        expected = []
        result = list(topic_service.all(get_data_func=get_data_func))

        self.assertEqual(expected, result)

    def test_getById_returns_TopicWhenPresent(self):
        get_data_func = lambda q, id: [(1, 'Title1', datestamp, 1, 1, 1)]
        expected = Topic(id=1, title='Title1', datestamp=datestamp, locked=1, category_id=1, user_id=1)
        result = topic_service.get_by_id(id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getById_return_None_when_NoData(self):
        get_data_func = lambda q, id: []
        expected = None
        result = topic_service.get_by_id(id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getMany_returns_ListOfTopics_when_DataIsPresent(self):
        get_data_func = lambda q: [(1, 'Title1', datestamp, 1, 1, 1), (2, 'Title2', datestamp, 1, 1, 1)]
        expected = [Topic(id=1, title='Title1', datestamp=datestamp, locked=1, category_id=1, user_id=1),
        Topic(id=2, title='Title2', datestamp=datestamp, locked=1, category_id=1, user_id=1)]
        result = topic_service.get_many(ids=[1,2], get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_getMany_returns_EmptyList_when_NoData(self):
        get_data_func = lambda q: []
        expected = []
        result = topic_service.get_many(ids=[], get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getByCategory_returns_ListOfTopics_when_DataisPresent(self):
        get_data_func = lambda q, id: [(1, 'Title1', datestamp, 1, 1, 1), (2, 'Title2', datestamp, 1, 1, 1)]
        expected = [Topic(id=1, title='Title1', datestamp=datestamp, locked=1, category_id=1, user_id=1),
        Topic(id=2, title='Title2', datestamp=datestamp, locked=1, category_id=1, user_id=1)]
        result = topic_service.get_by_category(category_id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_getByCategory_returns_emptyList_when_NoData(self):
        get_data_func = lambda q, id: []
        expected = []
        result = topic_service.get_by_category(category_id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getUserTopics_returns_listOfTopics_when_DataIsPresent(self):
        get_data_func = lambda q, id: [(1, 'Title1', datestamp, 1, 1, 1), (2, 'Title2', datestamp, 1, 1, 1)]
        expected = [Topic(id=1, title='Title1', datestamp=datestamp, locked=1, category_id=1, user_id=1),
        Topic(id=2, title='Title2', datestamp=datestamp, locked=1, category_id=1, user_id=1)]
        result = topic_service.get_user_topics(user_id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_getUserTopics_returns_emptyList_when_NoData(self):
        get_data_func = lambda q, id: []
        expected = []
        result = topic_service.get_user_topics(user_id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_create_createsTopic(self):
        topic = Topic(title='Title1', locked=1, category_id=1, user_id=1)
        insert_data_func = lambda q, topic: 1
        result = topic_service.create(topic=topic, insert_data_func=insert_data_func)

        self.assertEqual(topic, result)

    def test_update_updatesTopic(self):
        update_data_func = lambda q, a: None
        old_topic = Topic(id=1, title='Title1', datestamp=datestamp, locked=1, category_id=1, user_id=1)
        new_topic = Topic(id=2, title='Title2', datestamp=datestamp, locked=1, category_id=1, user_id=1)
        expected = Topic(
            id=old_topic.id, 
            title=new_topic.title, 
            datestamp=old_topic.datestamp, 
            locked=new_topic.locked, 
            category_id=new_topic.category_id, 
            user_id=old_topic.user_id)
        
        result = topic_service.update(old=old_topic, new=new_topic, update_data_func=update_data_func)

        self.assertEqual(expected, result)

    def test_lockUnlock_locksTopic(self):
        topic = Topic(id=1, title='Title1', datestamp=datestamp, locked=0, category_id=1, user_id=1)
        update_data_func = lambda q, topic: None

        expected = Topic(id=1, title='Title1', datestamp=datestamp, locked=1, category_id=1, user_id=1)
        result = topic_service.lock_unlock(topic=topic, update_data_func=update_data_func)

        self.assertEqual(expected, result)

    def test_exists_returns_True_when_ThereIsTopic(self):
        get_data_func = lambda q, id: [(1, 'Title1', datestamp, 1, 1, 1)]

        self.assertEqual(True, topic_service.exists(topic_id=1, get_data_func=get_data_func))

    def test_exists_returns_False_when_NoTopic(self):
        get_data_func = lambda q, id: []

        self.assertEqual(False, topic_service.exists(topic_id=1, get_data_func=get_data_func))
