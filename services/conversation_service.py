from data.models import Conversation
from data.database import insert_query, read_query, update_query

# def get_conversation_by_id(id: int):
#     data = read_query(
#         '''SELECT *
#            FROM cvonersations
#            WHERE id = ?''', (id,))
    
#     return next((Conversation.from_query_result(*row) for row in data), None)

def get_all_user_conversations(user_id: int):
    data = read_query(
        '''SELECT *
           FROM conversations 
           WHERE sender_id = ? OR recipient_id = ?''', (user_id, user_id))
    
    return (Conversation.from_query_result(*row) for row in data)