from datetime import datetime
from data.models import Topic, Reply, UserResponse, TopicResponse, Category
from data import database
from services import category_service
from services import user_service
from common.responses import NotFound

def all(key: str = None, search: str = None, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    if key is None and search is not None:
        data = get_data_func(
            '''SELECT id, title, datestamp, locked, category_id, user_id
               FROM topics
               WHERE title LIKE ?''', (f'%{search}%',))
    elif key is not None and search is not None:
        data = get_data_func(
            f'''SELECT id, title, datestamp, locked, category_id, user_id
               FROM topics
               WHERE {key} LIKE ?''', (f'%{search}%',))
    else:
        data = get_data_func(
            '''SELECT id, title, datestamp, locked, category_id, user_id
               FROM topics''')
    # data = database.read_query('''SELECT id, title, datestamp, locked, category_id, user_id FROM topics''')
    return (Topic.from_query_result(*row) for row in data)

def get_by_id(id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func(
        '''SELECT id, title, datestamp, locked, category_id, user_id
           FROM topics
           WHERE id = ?''', (id,))
    
    return next((Topic.from_query_result(*row) for row in data), None)

def get_many(ids: list[int], get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    ids_joined = ','.join(str(id) for id in ids)
    data = get_data_func(
        f'''SELECT id, title, datestamp, locked, category_id, user_id
            FROM topics
            WHERE id IN ({ids_joined})''')

    return [Topic.from_query_result(*row) for row in data]

def get_by_category(category_id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func(
        '''SELECT id, title, datestamp, locked, category_id, user_id
           FROM topics
           WHERE category_id = ?''', (category_id,))
        
    return [Topic.from_query_result(*row) for row in data]

def sort(topics: list[Topic], *, attribute): # not sure if we really need a sort for this one ???
    pass

def get_topic_replies(topic_id: int, get_data_func = None) -> list[Reply]:
    if get_data_func is None:
        get_data_func = database.read_query
    data = get_data_func(
        '''SELECT r.id, r.content, r.datestamp, r.upvotes, r.downvotes, r.best_reply, r.topic_id, r.user_id
           FROM replies AS r
           WHERE r.topic_id = ?''', (topic_id,))

    return [Reply.from_query_result(*row) for row in data]

def get_user_topics(user_id: int, get_data_func = None) -> list[Topic]:
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func(
        '''SELECT id, title, datestamp, locked, category_id, user_id
           FROM topics
           WHERE user_id = ?''', (user_id,))

    return [Topic.from_query_result(*row) for row in data]

def create(topic: Topic, insert_data_func = None):
    if insert_data_func is None:
        insert_data_func = database.insert_query

    generated_id = insert_data_func(
        '''INSERT INTO topics(title, datestamp, locked, category_id, user_id) VALUES(?,?,?,?,?)''',
        (topic.title, topic.datestamp, topic.locked, topic.category_id, topic.user_id))

    topic.id = generated_id

    return topic

def update(old: Topic, new: Topic, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    merged = Topic(
        id = old.id,
        title = new.title,
        datestamp = old.datestamp,
        locked = old.locked,
        category_id = new.category_id,
        user_id = old.user_id)

    update_data_func(
        '''UPDATE topics SET
           title = ?, locked = ?, category_id = ?
           WHERE id = ?''',
           (merged.title, merged.locked, merged.category_id, merged.id))

    return merged

def lock_unlock(topic: Topic, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    if topic.locked == 0:
        lock = 1
    else:
        lock = 0

    update_data_func(
        '''UPDATE topics SET
            locked = ?
            WHERE id = ?''', (lock, topic.id))

    topic.locked = lock
    
    return topic

def delete(topic: Topic, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    update_data_func('DELETE FROM topics WHERE id = ?', (topic.id,))    

def exists(topic_id: int, get_data_func = None):
    if get_data_func is None:
        get_data_func = database.read_query

    return any(get_data_func(
        '''SELECT id, title, datestamp, locked, category_id, user_id
           FROM topics
           WHERE id = ?''', (topic_id,)))

def create_response_object(topic: Topic):
    if topic.locked == 0:
        lock = False
    else:
        lock = True
    
    author = user_service.find_by_id(topic.user_id)
    category = category_service.get_by_id(topic.category_id)
    replies = get_topic_replies(topic.id)
    return TopicResponse(id=topic.id, author=author, title=topic.title, category=category, datestamp=topic.datestamp, replies=replies, locked=lock)