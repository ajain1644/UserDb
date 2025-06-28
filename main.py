from fastapi import FastAPI

from Apis.db_api import db_router
# from agent import tool_router
app = FastAPI()
app.include_router(db_router)       
# app.include_router(tool_router)       

@app.get("/")
def read_root():
    return {"message": "Hello World"}   

