from fastapi import FastAPI, APIRouter # cria aplicações web e organiza as rotas
from fastapi.middleware.cors import CORSMiddleware # permite q o front acesse a api
from contextlib import asynccontextmanager # gerencia ciclo de vida do recurso
from pydantic import BaseModel # define a estrutura dos dados que a api vai receber

from sqllite import run_sql
# importa run sql que roda os comandos sql
@asynccontextmanager # gerenciador de ciclo de vida da aplicação
async def lifespan(app: FastAPI): # roda durante a vida útil do app
    run_sql( # comando sql
        """
        CREATE TABLE IF NOT EXISTS users (
            id_users            SERIAL PRIMARY KEY,
            password_users      VARCHAR(255) NOT NULL,
            name_users          VARCHAR(255) NOT NULL,
            email_users         VARCHAR(255) NOT NULL
        )
        """
    )
    yield # pra coisas que ocupam muito espaço na memória do computador

app = FastAPI(lifespan=lifespan) # registra as rotas diretamente no app principal

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter() # registra as rotas diretamente no app principal

class User(BaseModel):  # a classe é a estrutura de dados que a API espera receber ao criar um novo usuário
    password_users: str
    name_users: str
    email_users: str

@router.get("/") # quando a requisição do tipo "get" for feita pro caminho "/", a função get users vai ser ativada
def get_users():
    return run_sql("SELECT * FROM users") # selecionar todos (*) os registros da tabela users e retorna o resultado
    # aí que entra o "Read" do crud, ele lê todos os users (dados) existentes na base de dados
    # o "SELECT * FROM users" diz, basicamente, lê todos esses users

@router.post("/users") # quando algúem fizer post no caminho "/users", vai ser ativada a função "create_users", ou seja, um user vai ser criado
def create_users(body: User): # argumento body pega o corpo (body) da requisição, que deve ser um JSON, e valida ele usando o modelo user pra que os dados estajam disponíveis no objeto body.
    password_users, name_users, email_users = body.password_users, body.name_users, body.email_users
    # objetos do body (atributos da classe user)
    return run_sql( # insere esses novos dados na tabela
        f"""
            INSERT INTO users(password_users, name_users, email_users) 
            VALUES('{password_users}', '{name_users}', '{email_users}')
        """
    )
    # aí que entra o "Create" do CRUD, usa o método post pra enviar dados e criar novos recursos
    # o "INSERT INTO users(password_users, name_users, email_users)" ta mandando criar um novo registro na tabela de users com esses atributos

app.include_router(router=router) # pega todas as rotas definidas no router e anexa ao app 
