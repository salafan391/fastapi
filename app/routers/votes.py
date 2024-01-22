from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. schemas import *
from .. import models
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List
from . import oauth2

router = APIRouter(prefix='/votes',tags=['votes'])

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(votes:Vote,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    query_vote=db.query(models.Votes).filter(models.Votes.post_id==votes.post_id,models.Votes.user_id==current_user.token_id)
    vote_found=query_vote.first()
    if (votes.post_dir == 1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.token_id} already voted on post {vote_found.post_id}")
        else:
            new_vote=models.Votes(post_id=votes.post_id,user_id=current_user.token_id)
            db.add(new_vote)
            db.commit()
            return {'success':'successfully voted'}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"vote does not exist")
        
        query_vote.delete(synchronize_session=False)
        db.commit()
        return {'success':'successfully deleted'}

