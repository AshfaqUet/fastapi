from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get('/')
def root():
    return {"message": "Welcome to my api"}

@app.get("/posts")
def get_post():
    return {"data": "These are your posts"}

@app.post("/posts")
def create_post(payload: dict = Body(...)):
    return payload