from flask import Flask, request, make_response, json
from newInstance import new_instance
from queries import get_winners, save_winner
from chat import chat

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/newSession', methods=["POST", "GET"])
def new_session():
    if request.method == "POST":
      session_json = json.dumps(new_instance())
      response = make_response(session_json)
      response.headers["Content-Type"] = "application/json"
      response.headers["Access-Control-Allow-Origin"] = "*"
      return response
    if request.method == "GET":
      return "New Session"
    
@app.route("/winners", methods=["POST"])
def winners():
    character = request.form.get("character")
    response = make_response(json.dumps(get_winners(character)))
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    print("request data: ", response)
    return response

@app.route("/addWinner", methods=["POST"])
def add_winner():
    id = request.form.get("id")
    character = request.form.get("character")
    username = request.form.get("username")
    print("request data: ", request.form)
    save_winner(id, username, character)
    return "Add Winner"

@app.route('/generate', methods=["POST"])
def generate():

    prompt = request.form.get("prompt")
    return chat(prompt)

if __name__ == '__main__':
    app.run()



