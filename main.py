from jsthon import JsthonDb
from fastapi import FastAPI
import uvicorn
import bcrypt
import models


api = FastAPI(title="cyberzonetask")
db = JsthonDb('reservations.json')


@api.post('/user/create')
def user_create(user: models.User):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(user.password,"UTF-8"), salt)
    user.password = str(hashed)
    db.choose_table('user')
    db.add(user.model_dump())
    db.choose_table(None)
    return {'SUCCES': user}


@api.post('/user/delete')
def user_delete(index: int):
    db.choose_table('user')

    def func1(data):
        if data['id'] == index:
            return True

    db.delete_with_function(func1)

    db.choose_table('booking')

    def func2(data):
        if data['user_id'] == index:
            return True

    db.delete_with_function(func2)

    db.choose_table(None)
    return {"SUCCES": True}


@api.post('/booking/create')
def booking_create(user: models.Booking):
    db.choose_table('booking')
    db.add(user.model_dump())
    db.choose_table(None)
    return {'SUCCES': user}


@api.post('/booking/delete')
def booking_delete(index: int):
    db.choose_table('booking')

    def func2(data):
        if data['id'] == index:
            return True

    db.delete_with_function(func2)

    db.choose_table(None)
    return {"SUCCES": True}


@api.get('/booking/get')
def booking_get():
    db.choose_table('booking')
    booking_list = db.show_table()
    booking_list.pop(0)
    db.choose_table(None)
    return {"SUCCES": booking_list}

if __name__ == "__main__":
    uvicorn.run("main:api", host="127.0.0.1", port=8000, reload=True)
