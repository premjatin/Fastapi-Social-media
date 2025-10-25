from typing import List, Optional

from sqlalchemy import func

from app import oauth2
from app import models,schemas
from app.database import get_db
from fastapi import Response, status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router=APIRouter( prefix= "/posts",tags=['Posts'])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user), # Use the correct type hint
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):

    # 1. Execute the query to get the list of tuples (Post, vote_count)
    posts_with_votes = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    # 2. THIS IS THE FIX: Manually transform the list of tuples into a list of dictionaries
    #    that matches the structure of your schemas.PostOut model.
    results = [{"Post": post, "votes": votes} for post, votes in posts_with_votes]

    return results

@router.post("/", status_code= status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post= cursor.fetchone()
    # conn.commit()
    new_post=models.Post(user_id=current_user.id ,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    # The query returns a single tuple: (Post, vote_count) or None
    result_tuple = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(models.Post.id == id).first()

    if not result_tuple:
        raise HTTPException(status_code=status.HTTP_4_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post, votes = result_tuple

    return {"Post": post, "votes": votes}

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    # id=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found")
    
    if post.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=" YOU DONT HAVE ACCESS")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post: schemas.PostCreate,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s,content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found")
    if post.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=" YOU DONT HAVE ACCESS")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()