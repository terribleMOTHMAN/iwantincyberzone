from fastapi import FastAPI
import uvicorn
import bcrypt
import models
from motor.motor_asyncio import AsyncIOMotorClient
from envparse import Env
from starlette.requests import Request

env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/reservation_database")
client = AsyncIOMotorClient(MONGODB_URL)
api = FastAPI()
api.state.mongo_client = client


@api.post('/user/create')
async def user_create(user: models.User, request: Request):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["reservation_database"]
    cursor = mongo_client.users.find({}).to_list(length=1000)
    fl = True
    for doc in await cursor:
        if doc["id"] == user.id:
            fl = False
            break
    if fl:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes(user.password,"UTF-8"), salt)
        user.password = str(hashed)
        await mongo_client.users.insert_one(user.model_dump())
        return {"SUCCES": True}
    else:
        return {"SUCCES": False}


@api.post('/user/delete')
async def user_delete(index: int, request: Request):
    mongo_users: AsyncIOMotorClient = request.app.state.mongo_client["reservation_database"]
    await mongo_users.users.delete_one({"id": index})
    await mongo_users.booking.delete_many({"user_id": index})
    return {"SUCCES": True}


@api.post('/booking/create')
async def booking_create(book: models.Booking, request: Request):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["reservation_database"]
    cursor = mongo_client.booking.find({}).to_list(length=1000)
    fl1 = True
    for doc in await cursor:
        if doc["id"] == book.id:
            fl1 = False
            break
    cursor = mongo_client.users.find({}).to_list(length=1000)
    fl2 = False
    for doc in await cursor:
        if doc["id"] == book.user_id:
            fl2 = True
            break
    if fl1 and fl2:
        await mongo_client.booking.insert_one(book.model_dump())
        return {'SUCCES': True}
    else:
        return {"SUCCES": False}


@api.post('/booking/delete')
async def booking_delete(index: int, request: Request):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["reservation_database"]
    await mongo_client.booking.delete_one({"id": index})
    return {"SUCCES": True}


@api.get('/booking/get')
async def booking_get(request: Request):
    booking_list = []
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["reservation_database"]
    cursor = mongo_client.booking.find({}).to_list(length=1000)
    for document in await cursor:
        document["_id"] = str(document["_id"])
        booking_list.append(document)
    return {"SUCCES": booking_list}

if __name__ == "__main__":
    uvicorn.run("main:api", host="127.0.0.1", port=8000, reload=True)
