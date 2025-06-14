

# Documentación oficial: https://fastapi.tiangolo.com/es/

# Instala FastAPI: pip install "fastapi[standard]" o "fastapi[all]"

from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles



app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="estatico")


# Url local: http://127.0.0.1:8000


@app.get("/")
async def root():
    return "Hola FastAPI"

# Url local: http://127.0.0.1:8000/url


@app.get("/url")
async def url():
    return  { "url":"https://mouredev.com/python" }

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Swagger: http://127.0.0.1:8000/redoc