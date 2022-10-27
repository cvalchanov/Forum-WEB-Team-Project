from pydantic import BaseModel, constr
from datetime import date, datetime

class Category(BaseModel):
    id: int | None
    name: str
    locked: bool = False
    private: bool = False

class Role:
    USER = 'user'
    ADMIN = 'admin'

TUsername = constr(regex='^\w{2,30}$')

class User(BaseModel):
    id: int | None
    username: TUsername
    password: str
    first_name: str
    last_name: str
    role: str | None = Role.USER

    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id: int, username: str, password: str, first_name: str, last_name: str, role: str):
        return cls(id=id, username=username, password=password, first_name=first_name, last_name=last_name, role=role)

class LoginData(BaseModel):
    username: TUsername
    password: str

class RegisterData(BaseModel):
    username: TUsername
    password: str
    firstname: str
    lastname: str
    role: str | None = Role.USER

class UserResponse(BaseModel):
    id: int
    username: str
    fullname: str
    role: str

class Message(BaseModel):
    id: int | None
    content: str
    datestamp: datetime
    user_id: int
    conversation_id: int

    @classmethod
    def from_query_result(cls, id: int, content: str, datestamp: datetime, user_id: int, conversation_id: int):
        return cls(id=id, content=content, datestamp=datestamp, user_id=user_id, conversation_id=conversation_id)

class Conversation(BaseModel):
    id: int | None
    sender_id: int
    recipient_id: int

    @classmethod
    def from_query_result(cls, id: int, sender_id: int, recipient_id: int):
        return cls(id=id, sender_id=sender_id, recipient_id=recipient_id)

class Reply(BaseModel):
    id: int | None
    content: str
    datestamp: datetime | None
    upvotes: int = 0
    downvotes: int = 0
    best_reply: bool = False
    topic_id: int
    user_id: int

    @classmethod
    def from_query_result(cls, id, content: str, datestamp: datetime, upvotes: int, downvotes: int, best_reply: bool, topic_id: int, user_id: int):
        return cls(id=id, content=content, datestamp=datestamp, upvotes=upvotes, downvotes=downvotes, best_reply=best_reply, topic_id=topic_id, user_id=user_id)

class Topic(BaseModel):
    id: int | None
    title: str
    datestamp: datetime | None
    locked: int = 0
    category_id: int
    user_id: int

    @classmethod
    def from_query_result(cls, id: int, title: str, datestamp: datetime, locked: int, category_id: int, user_id: int):
        return cls(id=id, title=title, datestamp=datestamp, locked=locked, category_id=category_id, user_id=user_id)

class TopicCreationData(BaseModel):
    topic_title: str
    category_id: int
    reply_content: str

class TopicResponse(BaseModel):
    id: int
    author: UserResponse
    title: str
    category: Category
    datestamp: datetime
    replies: list[Reply]
    locked: bool

class VotesCount(BaseModel):
    upvotes: int = 0
    downvotes: int = 0

class Vote(BaseModel):
    id: int | None
    user_id: int
    reply_id: int
    vote: bool

    @classmethod
    def from_query_result(cls, id: int, user_id: int, reply_id: int, vote: bool):
        return cls(id=id, user_id=user_id, reply_id=reply_id, vote=vote)
