from fastapi import APIRouter, Response, Header
from common.auth import get_user_or_raise_401
from services import conversation_service


conversations_router = APIRouter(prefix='/conversations')

@conversations_router.get('/')
def get_all_conversations(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    conversations = conversation_service.get_all_user_conversations(user.id)

    return conversations


