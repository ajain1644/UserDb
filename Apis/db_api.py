from fastapi import APIRouter
from pydantic import BaseModel
from Database.db import add_user, get_user, update_user, delete_user, get_all_users


class User(BaseModel):
    name: str
    email: str
    password: str


db_router = APIRouter(prefix="/users", tags=["users"])


@db_router.post("/adduser")
async def create_user(user: User):
    await add_user(user)
    return {"message": "User created successfully"}


@db_router.get("/getuser")
async def get_user_endpoint(user: User):
    result = await get_user(user)
    if result:
        return {"user": result, "message": "User found successfully"}
    else:
        return {"message": "User not found"}


@db_router.put("/updateuser")
async def update_user_endpoint(user: User):
    await update_user(user)
    return {"message": "User updated successfully"}


@db_router.delete("/deleteuser")
async def delete_user_endpoint(user: User):
    await delete_user(user)
    return {"message": "User deleted successfully"}


@db_router.get("/getallusers")
async def get_all_users_endpoint():
    users = await get_all_users()
    return users
