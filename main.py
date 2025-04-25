from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

from sqllite import run_sql

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_sql(
        """
        CREATE TABLE IF NOT EXISTS users (
            id_users            SERIAL PRIMARY KEY,
            password_users      VARCHAR(255) NOT NULL,
            name_users          VARCHAR(255) NOT NULL,
            email_users         VARCHAR(255) NOT NULL
        )
        """
    )
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

class User(BaseModel):
    password_users: str
    name_users: str
    email_users: str

@router.get("/")
def get_users():
    return run_sql("SELECT * FROM users")

@router.post("/users")
def create_users(body: User):
    password_users, name_users, email_users = body.password_users, body.name_users, body.email_users

    return run_sql(
        f"""
            INSERT INTO users(password_users, name_users, email_users) 
            VALUES('{password_users}', '{name_users}', '{email_users}')
        """
    )

app.include_router(router=router)
