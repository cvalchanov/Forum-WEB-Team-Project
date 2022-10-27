from data.models import Reply
from data.database import insert_query, read_query, update_query


def get_reply_by_id(id: int):
    data = read_query(
        '''SELECT *
            FROM replies 
            WHERE id = ?''', (id,))

    return next((Reply.from_query_result(*row) for row in data), None)


def create_reply(reply: Reply):
    generated_id = insert_query(
        'INSERT INTO replies(content,datestamp,upvotes,downvotes,best_reply,topic_id, user_id) VALUES(?,?,?,?,?,?,?)',
        (reply.content, reply.datestamp, reply.upvotes, reply.downvotes, reply.best_reply, reply.topic_id, reply.user_id))

    reply.id = generated_id

    return reply

def update_reply(old: Reply, new: Reply):
    merged = Reply(
        id=old.id,
        content=new.content or old.content,
        topic_id=new.topic_id or old.topic_id,
        datestamp=old.datestamp,
        upvotes=new.upvotes or old.upvotes,
        downvotes=new.downvotes or old.downvotes,
        best_reply=new.best_reply or old.best_reply,
        user_id=new.user_id or old.user_id
    )

    update_query(
        '''UPDATE replies SET
           content = ?, datestamp = ?, upvotes = ?, downvotes = ?, best_reply = ?, topic_id = ?, user_id = ?
           WHERE id = ? ''',
        (merged.content, merged.datestamp, merged.upvotes, merged.downvotes, merged.best_reply, merged.topic_id, merged.user_id, merged.id))

    return merged

def delete_reply(id: int):
    update_query('delete from replies where id = ?', (id,))

# def update_reply_vote_count(reply_id, upvote_data, downvote_data):
#     data = update_query(
#         '''UPDATE replies SET
#             upvote = ?,
#             downvote = ? 
#             WHERE vote_id = ?''', (upvote_data, downvote_data, reply_id))
