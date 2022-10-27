
from fastapi import APIRouter, Response, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest
from data.models import VotesCount
from services import vote_service, reply_service
# from common.responses import NotFound

votes_router = APIRouter(prefix='/t/{topic_id}')

@votes_router.get('/{reply_id}/upvote')
def get_upvotes_count(reply_id):
    # if category_id or topic id doesn't exist:
    #     return BadRequest('Some message')
    reply = reply_service.get_reply_by_id(reply_id)
    if not reply:
        return BadRequest()
    
    votes_count = vote_service.get_upvotes_by_reply(reply_id)
    
    return votes_count

@votes_router.get('/{reply_id}/downvote')
def get_downvotes_count(reply_id):
    # if category_id or topic id doesn't exist:
    #     return BadRequest('Some message')
    reply = reply_service.get_reply_by_id(reply_id)
    if not reply:
        return BadRequest()
        
    votes_count = vote_service.get_downvotes_by_reply(reply_id)

    return votes_count

@votes_router.put('/{reply_id}/upvote')
def update_upvote(reply_id, votes: VotesCount, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    reply = reply_service.get_reply_by_id(reply_id)
    if not reply:
        return BadRequest()

    existing_vote = vote_service.check_vote(user.user_id)
    
    if existing_vote is None:
        result = vote_service.create_vote(reply_id, user.user_id)
        vote_service.update_reply_vote_count(reply_id, votes)
    else:
        result = vote_service.update_vote(existing_vote.id, 1)
        
        vote_service.update_reply_vote_count(reply_id, votes)
        vote_service.update_vote()
    return result
        
@votes_router.put('/{reply_id}/downvote')
def update_downvote(reply_id, votes: VotesCount, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    reply = reply_service.get_reply_by_id(reply_id)

    if not reply:
        return BadRequest()
    # To check if user == None
    existing_vote = vote_service.check_vote(user.id)

    if existing_vote is None:
        result = vote_service.create_vote(reply_id, user.id)
        vote_service.update_reply_vote_count(reply_id, votes)
    else:
        result = vote_service.update_vote(existing_vote.id, 0)
        
        vote_service.update_reply_vote_count(reply_id, votes)
        vote_service.update_vote()
    # if result_update_reply_votes > -1:
    #     return votes
    # return result_update_reply_votes
    return result
