from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_models.required_pydantic import User, ToolSpec
from bson import ObjectId


MONGO_URI = "mongodb://admin:admin123@localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["user_db"]
user_collection = db["users"]
tool_collection = db["tools"]


def convert_objectid_to_str(doc):
    """Convert ObjectId to string and make document JSON serializable"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


async def add_user(user: User):
    await user_collection.insert_one(user.model_dump())
    return {"message": "User created successfully"}


async def get_user(user: User):
    result = await user_collection.find_one({"email": user.email})
    return convert_objectid_to_str(result) if result else None


async def update_user(user: User):
    await user_collection.update_one({"email": user.email}, {"$set": user.model_dump()})
    return {"message": "User updated successfully"}


async def delete_user(user: User):
    await user_collection.delete_one({"email": user.email})
    return {"message": "User deleted successfully"}


async def get_all_users():
    cursor = user_collection.find()
    users = await cursor.to_list(length=100)
    return [convert_objectid_to_str(user) for user in users]


async def add_tool(tool: ToolSpec):
    await tool_collection.insert_one(tool.model_dump())
    return {"message": "Tool created successfully"}


async def get_tool():
    result = tool_collection.find()
    return await result.to_list(length=None)
