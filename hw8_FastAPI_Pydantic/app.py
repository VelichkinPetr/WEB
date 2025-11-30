from datetime import datetime, timezone
from typing import Annotated, List

from annotated_types import MinLen, MaxLen
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field

app = FastAPI(title="Posts & Comments")

# POSTS = [
#     {
#         "id": int,
#         "title": str,
#         "description": str,
#         "created_at": str,
#         "comments": [
#             {
#                 "id": int,
#                 "text": str,
#                 "created_at": str
#             },
#             ....
#         ]
#     },
#     ....
# ]

class CommentCreate(BaseModel):
    text: Annotated[str, MinLen(5)]
    
class Comment(CommentCreate):
    id: int
    created_at: Annotated[datetime, datetime.now(timezone.utc)]

class PostCreate(BaseModel):
    title: Annotated[str, MinLen(5), MaxLen(255)]
    description: Annotated[str, MinLen(5)]

class Post(PostCreate):
    id: int
    created_at: Annotated[datetime, datetime.now(timezone.utc)]
    comments: List[Comment]

NEXT_POST_ID = 1
NEXT_COMMENT_ID = 1
POSTS: List[Post] = [

]

def check_post(post_id: int) -> Post:
    for post in POSTS:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

def check_comment(comment_id: int, post: Post = Depends(check_post)) -> Comment:
    for comment in post.comments:
        if comment.id == comment_id:
            return comment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')

@app.post("/posts", response_model=Post)
def create_post(data: PostCreate):
    global NEXT_POST_ID
    post = Post(
        id=NEXT_POST_ID,
        comments=[],
        created_at=datetime.now(timezone.utc),
        **data.model_dump()
    )
    POSTS.append(post)
    NEXT_POST_ID += 1
    return post

@app.get("/posts", response_model=List[Post])
def get_posts():
    return POSTS

@app.put('/posts/{post_id}', response_model=Post)
def update_post(data: PostCreate, post: Post = Depends(check_post)):
    for key, value in data.model_dump().items():
        setattr(post, key, value)
    post.created_at = datetime.now(timezone.utc)
    return post

@app.delete('/posts/{post_id}', response_model=Post)
def delete_post(post: Post = Depends(check_post)):
    POSTS.remove(post)
    return post

# дополнительно к CRUD для POSTS создать CRUD для комментариев к постам
# 
# GET /posts/{post_id}/comments
# POST /posts/{post_id}/comments
# GET /posts/{post_id}/comments/{comment_id}
# DELETE /posts/{post_id}/comments/{comment_id}
# PUT /posts/{post_id}/comments/{comment_id}

@app.post('/posts/{post_id}/comments', response_model=Comment)
def create_comment(data: CommentCreate, post: Post = Depends(check_post)):
    global NEXT_COMMENT_ID
    new_comment = Comment(
        id=NEXT_COMMENT_ID,
        created_at=datetime.now(timezone.utc),
        **data.model_dump()
    )
    post.comments.append(new_comment)
    NEXT_COMMENT_ID += 1
    return new_comment

@app.get('/posts/{post_id}/comments', response_model=list[Comment])
def get_comments(post: Post = Depends(check_post)):
    return post.comments

@app.get('/posts/{post_id}/comments/{comment_id}', response_model=Comment)
def get_comment(comment: Comment = Depends(check_comment)):
    return comment

@app.put('/posts/{post_id}/comments/{comment_id}', response_model=Comment)
def update_comment(data: CommentCreate, comment: Comment = Depends(check_comment)):
    for key, value in data.model_dump().items():
        setattr(comment, key, value)
    comment.created_at = datetime.now(timezone.utc)
    return comment

@app.delete('/posts/{post_id}/comments/{comment_id}', response_model=Comment)
def delete_comment(post: Post = Depends(check_post), comment: Comment = Depends(check_comment)):
    post.comments.remove(comment)
    return comment
