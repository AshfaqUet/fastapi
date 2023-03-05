import time

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:  # try to connect to db after some time untill successfully connected
    try:
        # Connect to an existing database
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres',
                                cursor_factory=RealDictCursor)

        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database connection is successfull")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error! ", error)
        time.sleep(5)

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
        if p["id"] == id:
            return i


@app.get('/')
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_post():
    cursor.execute("SELECT * from posts;")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    cursor.execute("SELECT * FROM posts where id = %s", (str(post_id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")

    return {"data": post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    cursor.execute("DELETE FROM posts where id = %s returning *", (str(post_id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *",
                   (post.title, post.content, post.published, str(post_id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")

    return {"data": updated_post}
