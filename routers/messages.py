from fastapi import APIRouter
from data.models import Message
from services import message_service, conversation_service
from common.responses import BadRequest, NotFound, NoContent

messages_router = APIRouter(prefix='/conversations')


@messages_router.get('/{coversation_id}')
def get_messages(coversation_id: int):
    conversation = conversation_service.get_conversation_by_id(coversation_id)
    if not conversation:
        return BadRequest()
        
    messages = message_service.all()
    if messages == None:
        return NoContent()

    return messages

# gets all messages 

@messages_router.get('/{coversation_id}/{message_id}')
def get_message_by_id(coversation_id: int, message_id):
    conversation = conversation_service.get_conversation_by_id(coversation_id)
    if not conversation:
        return BadRequest()

    result = message_service.get_message_by_id(message_id)

    if result is None:
        return NotFound()
    else:
        return result

@messages_router.post('/{coversation_id}', status_code=201)
def create_message(coversation_id: int, message: Message):
    conversation = conversation_service.get_conversation_by_id(coversation_id)
    if not conversation:
        return BadRequest()

    return message_service.create_message(message)

@messages_router.put('/{coversation_id}/{message_id}')
def update_message(coversation_id: int, message_id, message: Message):
    conversation = conversation_service.get_conversation_by_id(coversation_id)
    if not conversation:
        return BadRequest()

    result = message_service.get_message_by_id(message_id)
    if result is None:
        return NotFound()
    
    return message_service.update_message(message_id, message)

@messages_router.delete('/{coversation_id}/{message_id}')
def delete_message(coversation_id: int, message_id: int):
    conversation = conversation_service.get_conversation_by_id(coversation_id)
    if not conversation:
        return BadRequest()

    message_service.delete_message(message_id)

    return NoContent()