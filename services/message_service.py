from data.models import Message
from data.database import insert_query, read_query, update_query

def all():
    data = read_query('select * from messages')

    return (Message.from_query_result(*row) for row in data)

def get_message_by_id(id):
    data = read_query(
        '''SELECT *
           FROM messages
           WHERE id = ?''', (id,))
    
    return next((Message.from_query_result(*row) for row in data), None)

# def check_message(user_id):
#     # if not found this is first vote of the user on this reply
#     data = read_query(
#         '''SELECT vote
#            FROM votes
#            WHERE user_id = ?
#         ''', 
#         (user_id,)
#     )

#     return data

def create_message(message: Message):
    generated = insert_query(
        'INSERT INTO messages(content, datestamp, user_id, conversation_id) VALUES(?,?,?,?)',
        (message.content, message.datestamp, message.user_id, message.conversation_id))

    return generated

def update_message(int, message: Message):
    data = update_query(
        '''UPDATE messages SET
            content = ?,
            datestamp = ?,
            user_id = ?,
            conversation_id = ?
            WHERE id = ?''', (message.content, message.datestamp, message.user_id, message.conversation_id))
    
    return next((Message.from_query_result(*row) for row in data), None)

def delete_message(id):
    update_query('delete from messages where id = ?', (id,))
