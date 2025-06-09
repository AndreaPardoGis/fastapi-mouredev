# Instala pydantic: pip install pydantic

### Users API ###

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Inicia el server: uvicorn users:app --reload

# Entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Andrea", surname="Pardo", url="https://google.es", age=32),
              User(id=2, name="Adria", surname="Minguez", url="https://google.com", age=35),
              User(id=3, name="Greta", surname="Van", url="https://google.com.es", age=2)]


@app.get("/usersjson")
async def usersjson():  # creamos un json a mano
    return [{"name": "Andrea", "surname": "Pardo", "url": "https://google.es", "age": "32"},
            {"name": "Adria", "surname": "Minguez", "url": "https://google.com", "age": "35"},
            {"name": "Greta", "surname": "Van", "url": "https://google.com.es", "age": "2"},]


@app.get("/users")
async def users():
    return users_list

@app.get("/user/{id}")  # Path
async def user(id: int):
    return search_user(id)   


@app.get("/user/")  # Query
async def user(id: int):
    return search_user(id)

@app.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    users_list.append(user)
    return user

@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    return user

@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
        
    if not found:
        return {"error": "No se ha eliminado el usuario"}
            


def search_user(id: int):
    users = filter(lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}


