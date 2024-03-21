from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def Landing():
    return "Welcome to my first Flask api"

store = [{
    'name' : 'chair',
    'price' : 120
},
{
    'nmae' : 'table',
    'price' : 200
}]

@app.route('/store', methods= ["POST"])
def check():
    data = request.json
    username = data.get('username', '')
    if username == 'Imisioluwa23':
        return store
    else:
        return "Intruder alert"
    
