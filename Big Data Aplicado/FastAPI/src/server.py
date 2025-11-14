from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/users/")
async def read_users():
    return {"users": ["Alice", "Bob", "Charlie"]}