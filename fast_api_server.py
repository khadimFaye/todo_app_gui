
from ctypes import Union
from curses.ascii import isalpha
from fastapi import FastAPI
import uvicorn 
from pydantic import BaseModel
from database import Database
db=Database()
class Users(BaseModel):
    nome_utente: str
    password : str

app = FastAPI()
@app.post("/send-data")
def read_root(user : Users ):
    db.add_user(user.nome_utente,user.password)
    print (user.nome_utente,user.password)

@app.get('/get_by_name{user_name}')
def get_user(user_name : str):
    if user_name == Users.name:
        return {'user_name':user_name}
if __name__ == '__main__':
    uvicorn.run('fast_api_server:app',host = '127.0.0.1',port = 8000,reload =True)
