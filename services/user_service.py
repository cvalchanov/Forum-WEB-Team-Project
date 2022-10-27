from data.database import insert_query, read_query
from data.models import Role, User
from mariadb import IntegrityError
from common.responses import NotFound
from data import database


_SEPARATOR = ';'

# passwords should be secured as hashstrings in DB
def _hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(username: str, get_data_func = None) -> User | None:
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func(
        'SELECT id, username, password, firstname, lastname, role FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)

def find_by_id(id: int, get_data_func = None) -> User | None:
    if get_data_func is None:
        get_data_func = database.read_query

    data = get_data_func(
        'SELECT id, username, password, firstname, lastname, role FROM users WHERE id = ?', (id,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    password = _hash_password(password)
    return user if user and user.password == password else None


def create(username: str, password: str, firstname: str, lastname: str, role: str, insert_data_func = None) -> User | None:
    if insert_data_func is None:
        insert_data_func = database.insert_query

    password = _hash_password(password)
    try:
        generated_id = insert_data_func(
            'INSERT INTO users(username, password, firstname, lastname, role) VALUES (?,?,?,?,?)',
            (username, password, firstname, lastname, role))

        return User(id=generated_id, username=username, password='', first_name=firstname, last_name=lastname, role=role)

    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None

def promote_demote(user: User, update_data_func = None):
    if update_data_func is None:
        update_data_func = database.update_query

    if not user.is_admin():
        role = Role.ADMIN
    else:
        role = Role.USER

    update_data_func(
        '''UPDATE users SET
            role = ?
            WHERE id = ?''', (role, user.id))
    
    user.role = role

    return user


def create_token(user: User) -> str:
    # note: this token is not particulary secure, use JWT for real-world uses
    return f'{user.id}{_SEPARATOR}{user.username}'


def is_authenticated(token: str, get_data_func = None) -> bool:
    if get_data_func is None:
        get_data_func = database.read_query

    id, username = token.split(_SEPARATOR)
    return any(get_data_func(
        'SELECT 1 FROM users where id = ? and username = ?',
        # note: this token is not particulary secure, use JWT for real-world user
        (id, username)))


def from_token(token: str) -> User | None:
    _, username = token.split(_SEPARATOR)

    return find_by_username(username)
