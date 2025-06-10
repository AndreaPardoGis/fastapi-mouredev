# Instala pydantic: pip install pydantic

### Users API ###

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


# Inicia el server: uvicorn users:app --reload
router = APIRouter(prefix="/users", 
                   tags=["users"])



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


@router.get("/usersjson")
async def usersjson():  # creamos un json a mano
    return [{"name": "Andrea", "surname": "Pardo", "url": "https://google.es", "age": "32"},
            {"name": "Adria", "surname": "Minguez", "url": "https://google.com", "age": "35"},
            {"name": "Greta", "surname": "Van", "url": "https://google.com.es", "age": "2"},]


@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")  # Path
async def user(id: int):
    return search_user(id)   


@router.get("/user/")  # Query
async def user(id: int):
    return search_user(id)

@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.append(user)
    return user

# cambiar los not found por las excepciones y los errores,
# docu:  https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
# docu codigo errores: https://developer.mozilla.org/es/docs/Web/HTTP/Reference/Status

@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    return user

@router.delete("/user/{id}")
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


