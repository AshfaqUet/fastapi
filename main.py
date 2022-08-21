from email import message
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


my_posts = [
    {
        "id": 1,
        "title": "title here",
        "content": "content here"
    },
    {
        "id": 2,
        "title": "title 2 here",
        "content": "content 2 here"
    }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
     for i, p in enumerate(my_posts):
        if p["id"]==id:
            return i


@app.get('/')
def root():
    return {"message": "Welcome to my api"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(3, 2000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}

@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    post = find_post(post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")

    return {"data": post}

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    index = find_index_post(post_id)
    if index:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return Response(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id {post_id} does not exist")

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    index = find_index_post(post_id)
    if index:
        post_dict = post.dict()
        post_dict["id"] = post_id
        my_posts[index] = post_dict
        return {"data": post_dict}
    
    return Response(status_code=status.HTTP_400_BAD_REQUEST)

