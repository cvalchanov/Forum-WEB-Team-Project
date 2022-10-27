from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NoContent, NotFound, Unauthorized
from services import topic_service
from services import category_service
from services import user_service
from services import reply_service
from data.models import Reply, Topic, TopicResponse, Category, UserResponse, TopicCreationData
from datetime import datetime

topics_router = APIRouter(prefix='/topics')

@topics_router.get('/', response_model=list[Topic])
def get_topics(key: str | None = None, search: str | None = None):
    return topic_service.all(key, search)

@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = topic_service.get_by_id(id)

    if topic is None:
        return NotFound()
    else:
        replies = topic_service.get_topic_replies(id)
        category = category_service.get_by_id(topic.category_id)
        user = user_service.find_by_id(topic.user_id)
        user_response = UserResponse(id=user.id, username=user.username, fullname=(f'{user.first_name} {user.last_name}'), role=user.role)
        if topic.locked == 0:
            locked = False
        else:
            locked = True

        return TopicResponse(id=topic.id, author=user_response, title=topic.title, category=category, datestamp=topic.datestamp, replies=replies, locked=locked)

@topics_router.post('/', status_code=201)
def create_topic(topic: TopicCreationData, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    category = category_service.get_by_id(topic.category_id)
    datestamp = datetime.now()
    if (category and user) and not category.locked:
        topic_model = Topic(title=topic.topic_title, datestamp=datestamp, category_id=topic.category_id, user_id=user.id)
        new_topic = topic_service.create(topic_model)
        reply_model = Reply(content=topic.reply_content, datestamp=datestamp, topic_id=new_topic.id, user_id=user.id)
        new_reply = reply_service.create_reply(reply_model)
        author = UserResponse(id=user.id, username=user.username, fullname=(f'{user.first_name} {user.last_name}'), role=user.role)
        return TopicResponse(
            id=new_topic.id, 
            author=author, 
            title=new_topic.title, 
            category=category, 
            datestamp=new_topic.datestamp,
            replies=[new_reply],
            locked=new_topic.locked)
    else:
        return BadRequest()

@topics_router.put('/{id}')
def update_topic(id: int, topic: Topic, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    existing_topic = topic_service.get_by_id(id)

    if existing_topic and existing_topic.user_id == user.id:
        return topic_service.update(existing_topic, topic)
    elif existing_topic and existing_topic.user_id != user.id:
        return Unauthorized()
    else:
        return NotFound()

@topics_router.patch('/{id}/lock')
def lock_unlock_topic(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(id)
    if topic and user.is_admin():
        return topic_service.lock_unlock(topic)
    elif not topic:
        return NotFound()
    else:
        return Unauthorized()

@topics_router.delete('/{id}')
def delete_topic(id: int, x_token: str = Header()):
    topic = topic_service.get_by_id(id)
    user = get_user_or_raise_401(x_token)
    if topic and user.is_admin():
        topic_service.delete(topic)
        return NoContent()
    elif not topic:
        return NotFound()
    else:
        return Unauthorized()

