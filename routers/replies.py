
from fastapi import APIRouter, Response, Header
from common.auth import get_user_or_raise_401
from data.models import Reply
from services import reply_service, topic_service
from common.responses import BadRequest, NotFound, Unauthorized

replies_router = APIRouter(prefix='/t/{topic_id}')

@replies_router.post('/', status_code=201)
def create_reply(reply: Reply):
    topic = topic_service.get_by_id(reply.topic_id)
    if not topic or topic.locked:
        return BadRequest()

    return reply_service.create_reply(reply)

@replies_router.get('/{id}')
def get_reply_by_id(id: int):
    result = reply_service.get_reply_by_id(id)

    if result is None:
        return NotFound()
    
    return result

@replies_router.put('/{id}')
def update_reply(id: int, reply: Reply, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(reply.topic_id)
    if not topic or topic.locked:
        return BadRequest()

    if reply.user_id != user.id:
        return Unauthorized()
    
    result = reply_service.get_reply_by_id(id)
    
    if result is None:
        return NotFound()
    
    return reply_service.update_reply(result, reply)

@replies_router.delete('/{id}')
def delete_reply(id: int, reply: Reply, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = topic_service.get_by_id(reply.topic_id)
    if not topic or topic.locked:
        return BadRequest()

    if reply.user_id != user.id:
        return Unauthorized()
        
    reply_service.delete_reply(id)

    return NotFound()
