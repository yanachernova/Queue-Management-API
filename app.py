import os
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db
from adminqueue import AdminQueue

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
CORS(app)

aq = AdminQueue()

@app.route('/')
def home():
    return render_template('index.html', name="home")

@app.route('/new', methods=['POST'])
def enqueue():
    if not request.json.get('name'):
        return jsonify({"name": "is required"}), 422
    if not request.json.get('phone'):
        return jsonify({"phone": "is required"}), 422

    item = {
        "name": request.json.get('name'),
        "phone": request.json.get('phone')
    }

    msg = aq.enqueue(item)
    
    return jsonify(msg), 200

@app.route('/next', methods=['GET'])
def dequeue():
    item = aq.dequeue()
    return jsonify({"msg":"Procesado siguiente en la fila", "item": item}), 200

@app.route('/all', methods=['GET'])
def queue():
    fila = aq.get_queue()
    return jsonify(fila), 200

if __name__ == "__main__":
    manager.run()