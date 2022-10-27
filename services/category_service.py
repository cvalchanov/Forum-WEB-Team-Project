from data.database import insert_query, read_query, update_query
from data.models import Category, Topic
from routers import categories

def all():
    data = read_query('select id, name, locked from categories order by id')

    return (Category(id=id, name=name, locked=locked) for id, name, locked in data)


def search(search: str = None):
    if search is None:
        data = read_query(
            '''select id, name from categories''')
    else:
        data = read_query(
            '''select id, name
               from categories 
               where name like ?''', (f'{search}%',))

    category = (Category(id=id, name=name) for id, name in data)

    return [
        categories.CategoryResponseModel(
            category = category,
            topics = get_topics(category.id))
        for category in category] 


def sort(lst: list[Category], reverse=False):
    return sorted(
        lst,
        key=lambda p: p.name,
        reverse=reverse)



def get_by_id(id: int):
    data = read_query('select id, name, locked from categories where id = ?', (id,))

    return next((Category(id=id, name=name, locked=locked) for id, name, locked in data), None)



def exists(id: int):
    return any(
        read_query(
            'select id, name from categories where id = ?',
            (id,)))


def create(category: Category):
    generated_id = insert_query(
        'insert into categories(name) values(?)',
        (category.name,))

    category.id = generated_id

    return category



def get_by_category(category_id: int):
    data = read_query(
        '''select title, id from topics where categories_id = ?''', (category_id,))

    return (Topic.from_query_result(*row) for row in data)


def get_topics(category_id: int, get_data_func = None) -> list[Topic]:
    if get_data_func is None:
        get_data_func = read_query
    data = get_data_func(
        '''select t.id, t.title, t.datestamp, t.locked, t.categories_id, users_id
           from topics AS t
           where t.categories_id = ?''', (category_id,))

    return [Topic.from_query_result(*row) for row in data]





def delete(category_id: int):
    update_query('delete from categories where id = ?', (category_id,))


def update(old: Category, new: Category, update_data_func = None):
    if update_data_func is None:
        update_data_func = update_query

    merged = Category(
        id = old.id,
        name = new.name or old.name,
        locked = new.locked or old.locked)

    update_data_func(
        '''update categories set
           name = ?, locked = ?
           where id = ?''',
           (merged.name, merged.locked, merged.id))

    return merged

def lock_unlock(category: Category, update_data_func = None):
    if update_data_func is None:
        update_data_func = update_query

    if category.locked == False:
        key = True 
    else:
        key = False

    update_data_func(
        '''update categories set
            locked = ?
            where id = ?''', (key, category.id))

    category.locked = key
    
    return category
