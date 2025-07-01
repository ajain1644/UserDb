from fastapi import FastAPI
from Apis.db_api import db_router
app = FastAPI()
app.include_router(db_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
