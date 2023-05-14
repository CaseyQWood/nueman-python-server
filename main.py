import datetime
from flask import Flask, request, make_response, json

from typing import Tuple, Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime

from newInstance import new_instance
from queries import get_winners, save_winner, update_messages
from chat import chat
from embedding import get_embedding

app = FastAPI()

# app = Flask(__name__)

@app.get("/")
def root():
    return {"Hello": "World"}

class Session(BaseModel):
    id: int
    prompt: str

@app.post("/embeddings")
def embeddings(sesh: Session) -> JSONResponse:
    print("request data: ", sesh)
    response_data = {
        "message": "Embeddings",
        "id": sesh.id,
        "prompt": sesh.prompt
    }
    return JSONResponse(content=response_data)

@app.post('/newSession')
def new_session() -> Tuple[int, str]:
    print("New Session: ", datetime.now().hour, ":", datetime.now().minute, ":", datetime.now().second)
    return new_instance()

    
# @app.post("/winners")
# def winners():
#     character = request.form.get("character")
#     response = make_response(json.dumps(get_winners(character)))
#     response.headers["Content-Type"] = "application/json"
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     print("request data: ", response)
#     return response

# @app.post("/addWinner")
# def add_winner():
#     id = request.form.get("id")
#     character = request.form.get("character")
#     username = request.form.get("username")
#     print("request data: ", request.form)
#     save_winner(id, username, character)
#     return "Add Winner"

# @app.post('/generate')
# def generate():
#     request_id = request.form.get("id")
#     prompt = request.form.get("prompt")

#     # await update_messages(request_id, prompt)
    
#     print("request id: ", request_id)
#     print("request prompt: ", prompt)

#     return chat(prompt)

# if __name__ == '__main__':
#     app.run()



