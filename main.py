from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def root():
    return {"message": "Welcome to my api"}

@app.get("/posts")
def get_post():
    return {"data": "These are your posts"}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.post("/posts")
def create_post(post: Post):
    print(post.title)
    print(post.content)

    # pydantic model to dict
    print(post.dict())
    return {"data": post}