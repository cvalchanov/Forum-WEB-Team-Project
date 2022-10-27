from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.auth import get_user_or_raise_401
from data.models import Category, Topic
from services import category_service
from common.responses import NotFound, NoContent, Unauthorized


class CategoryResponseModel(BaseModel):
    category: Category
    topics: list[Topic]


categories_router = APIRouter(prefix='/categories')


@categories_router.get('/')
def get_categories(sort: str | None = None, search: str | None = None):
    categories = category_service.all()
    if categories == None:
        return NoContent()

    if search:
        return category_service.search(search)
        
    if sort and (sort == 'asc' or sort == 'desc'):
        return category_service.sort(categories, reverse=sort == 'desc')
    

    return [
        CategoryResponseModel(
            category = category,
            topics = category_service.get_topics(category.id))
        for category in category_service.all()]

# gets all categories, sort and search are optional 
# sort = asc/desc by id, which is chronically correct, search by first letters)



@categories_router.get('/{id}')
def get_category_by_id(id: int):
    category = category_service.get_by_id(id)

    if category is None:
        return NotFound()
    else:
        return CategoryResponseModel(
            category=category,
            topics=category_service.get_topics(category.id))

# gets a category by id



@categories_router.post('/')
def create_category(category: Category, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if user.is_admin():
        created_category = category_service.create(category)
        return CategoryResponseModel(category=created_category, topics=[])
    else: 
        return Unauthorized()

# creates a category, only "name" is required, "id" is generated and "locked" is false by default 
# example body: {"name": "Gardening"}
# requires x-token of an admin user



@categories_router.put('/{id}')
def update_category(id: int, category: Category, x_token: str = Header()):
    existing_category = category_service.get_by_id(id)
    user = get_user_or_raise_401(x_token)
    
    if existing_category and user.is_admin():
        return category_service.update(existing_category, category)
    elif not existing_category: 
        return NotFound()
    else:
        return Unauthorized()

# updates a category by id, "name" and "locked" can be changed
# example body: {"name": "Gardening for beginners", "locked": "true"}
# requires x-token of an admin user

@categories_router.patch('/{id}/lock')
def lock_unlock_category(id: int, x_token: str = Header()):
    category = category_service.get_by_id(id)
    user = get_user_or_raise_401(x_token)
    if category and user.is_admin():
        return category_service.lock_unlock(category)
    elif not category:
        return NotFound()
    else: 
        return Unauthorized()

# updates a category by id, changes only "locked" to the opposite boolean value (True -> False and vice-versa)
# no body needed
# requires x-token of an admin user


@categories_router.delete('/{id}')
def delete_category_by_id(id: int, x_token: str = Header()):
    category = category_service.get_by_id(id)
    user = get_user_or_raise_401(x_token)
    if category and user.is_admin():
        category_service.delete(id)
        return NoContent()
    elif not category: 
        return NotFound()
    else:
        return Unauthorized()

# deletes a category by id, but only if the category is empty
# no body needed
# requires x-token of an admin user