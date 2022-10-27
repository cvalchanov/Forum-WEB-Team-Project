from data.models import Reply, Vote, VotesCount
from data.database import insert_query, read_query, update_query

def get_upvotes_by_reply(reply_id):
    data = read_query(
        '''SELECT *
            FROM replies 
            WHERE id = ?''', (reply_id,))

    reply = next((Reply.from_query_result(*row) for row in data), None)
    return reply.upvotes

def get_downvotes_by_reply(reply_id):
    data = read_query(
        '''SELECT *
            FROM replies 
            WHERE id = ?''', (reply_id,))

    reply = next((Reply.from_query_result(*row) for row in data), None)

    return reply.downvotes

def check_vote(user_id):
    # if not found this is first vote of the user on this reply
    data = read_query(
        '''SELECT *
           FROM votes
           WHERE user_id = ?
        ''', 
        (user_id,)
    )
    return next((Vote.from_query_result(*row) for row in data), None)

def create_vote(reply_id, user_id, vote_data):
    generated = insert_query(
        'INSERT INTO votes(user_id, reply_id, vote) VALUES(?,?,?)',
        (reply_id, user_id, vote_data))

    return generated

def update_vote(vote_id, vote_data):
    data = update_query(
        '''UPDATE votes SET
            vote = ? 
            WHERE vote_id = ?''', (vote_data, vote_id))
    
    # return next((Reply.from_query_result(*row) for row in data), None)
    return data

def update_reply_vote_count(reply_id, votes: VotesCount):
    data = update_query(
        '''UPDATE replies SET
            upvotes = ?,
            downvotes = ? 
            WHERE id = ?''', (votes.upvotes, votes.downvotes, reply_id))
    
    return data

def delete_vote(id):
    update_query('delete from votes where id = ?', (id,))
