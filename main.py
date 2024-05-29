from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
#////Importando rutas ///////////////////
from routers.modify_client import modify_client

app = FastAPI()

#/////Agregando la ruta al route
app.include_router(modify_client)


origins = [
    "http://localhost",
    "http://localhost:49229",
    "http://127.0.0.1",
    "http://127.0.0.1:49229",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "10.7.110.233:8000",
    "10.7.110.233:3000",
    "10.7.110.233",
    "https://conext.smartolt.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return HTTPException(status_code=202, detail="ms_running")




