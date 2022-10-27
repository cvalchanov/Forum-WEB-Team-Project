from fastapi import FastAPI
from routers.categories import categories_router
from routers.replies import replies_router
from routers.topics import topics_router
from routers.users import users_router
from routers.votes import votes_router
from routers.conversations import conversations_router
from routers.messages import messages_router


app = FastAPI()
app.include_router(categories_router)
app.include_router(replies_router)
app.include_router(topics_router)
app.include_router(users_router)
app.include_router(votes_router)
app.include_router(conversations_router)
app.include_router(messages_router)