import os
import datetime

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(os.getcwd(), 'data/todos.db')
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    timing = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Todo {self.title} at {self.timing}>'


@app.route('/')
def home():
    return "<h1>Welcome to Simple Todo Manager API</h1>"


@app.route('/api/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        if not request.json or not 'title' in request.json:
            abort(400)

        newTodo = Todo(title=request.json['title'],
                       timing=datetime.datetime.now())
        db.session.add(newTodo)
        db.session.commit()

    data = Todo.query.all()
    print(data)

    return jsonify({'todos': list(map(lambda todo: {'id': todo.id, 'title': todo.title, 'timing': todo.timing}, data))})
