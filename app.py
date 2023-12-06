from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://riken:admin28@localhost:5432/flask_database'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    #table__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    with app.app_context():
        db.create_all()


@app.route('/tasks')
def get_tasks():
    tasks = Task.query.all()
    task_list = [
        {'id': task.id, 'title': task.title, 'done':task.done} for task in tasks
    ]
    return jsonify({"tasks":task_list})

@app.route('/tasks', methods=['post'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], done=data['done'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'Message':'Task created'}), 201




if __name__== '__main__':
    app.run(debug=True)
