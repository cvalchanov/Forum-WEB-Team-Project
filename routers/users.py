from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest, NotFound, Unauthorized
from data.models import LoginData, UserResponse, Topic, RegisterData, Role
from services import user_service
from services import topic_service


users_router = APIRouter(prefix='/users')


@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.username, data.password)

    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')


@users_router.get('/info')
def user_info(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    return UserResponse(id=user.id, username=user.username, fullname=(f'{user.first_name} {user.last_name}'), role=user.role)


@users_router.get('/topics', response_model=list[Topic])
def user_topics(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    return topic_service.get_user_topics(user.id)


@users_router.post('/register')
def register(data: RegisterData):
    user = user_service.create(data.username, data.password, data.firstname, data.lastname, data.role)
    if user:
        user_response = UserResponse(id=user.id, username=user.username, fullname=(f'{user.first_name} {user.last_name}'), role=user.role)
    else:
        user_response = None
    return user_response or BadRequest(f'Username {data.username} is taken.')

@users_router.patch('/{id}/admin')
def promote_demote(id: int, x_token: str = Header()):
    user_promoting_demoting = get_user_or_raise_401(x_token)
    targeted_user = user_service.find_by_id(id)

    if user_promoting_demoting and targeted_user and user_promoting_demoting.is_admin() :
        user_service.promote_demote(targeted_user)
        return UserResponse(id=targeted_user.id, username=targeted_user.username, fullname=(f'{targeted_user.first_name} {targeted_user.last_name}'), role=targeted_user.role)
    elif not user_promoting_demoting or not targeted_user:
        return NotFound()
    elif not user_promoting_demoting.is_admin():
        return Unauthorized()