from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. schemas import *
from .. import models
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List
from . import oauth2
from sqlalchemy import func

router = APIRouter(prefix='/posts',
                   tags=['posts'])


# @router.get("/",response_model=List[PostResponse])
@router.get("/")
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
            limit:int=5,skip:int=0,
            search:Optional[str]=''):
    posts = db.query(models.Post).filter(models.Post.owner_id==current_user.token_id)
    posts = posts.filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    results = db.query(models.Post,func.count(models.Votes.post_id).label('votes')).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = [(post, votes) for post, votes in results]
    return results
   


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=PostResponse)
def post(post:Post,db:Session=Depends(get_db),
         current_user:int=Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.token_id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/latest')
def get_latest_post(db:Session=Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post

@router.get('/{item_id}',response_model=PostResponse)
def get_singal_post(item_id,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==item_id).first()
 
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {item_id} was not found") 
    return post

           


@router.delete('/{item_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(item_id,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==item_id)
    my_post = post.first()
    if my_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with index {item_id} was not found")
    if my_post.owner_id != user_id.token_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized to perform request action')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{item_id}',status_code=status.HTTP_202_ACCEPTED,response_model=PostResponse)
def update_post(item_id:str,post:Post,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    get_post = db.query(models.Post).filter(models.Post.id==item_id)
    my_post = get_post.first()
    if my_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {item_id} was not found")
    if my_post.owner_id != user_id.token_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized to perform request action')
    get_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
    return get_post.first()
