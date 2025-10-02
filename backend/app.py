from flask import Flask, request, jsonify, current_app
from flask_cors import CORS

import os
import psycopg2

def create_app(test_config=None, test_conn=None):
    app = Flask(__name__)
    CORS(app)

    if test_conn:
        conn = test_conn
    else:
        # Database connection
        DB_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
        DB_NAME = os.environ.get('POSTGRES_DB', 'todos')
        DB_USER = os.environ.get('POSTGRES_USER', 'todo_user')
        DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'todo_pass')
        conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    app.config['conn'] = conn
    # Register routes
    app.route('/todos', methods=['GET'])(get_todos)
    app.route('/todos', methods=['POST'])(add_todo)
    app.route('/todos/<int:todo_id>', methods=['PUT'])(update_todo)
    app.route('/metrics')(metrics)
    return app

def get_todos():
    cur = current_app.config['conn'].cursor()
    cur.execute('SELECT id, text, done FROM todos')
    todos = [{'id': row[0], 'text': row[1], 'done': row[2]} for row in cur.fetchall()]
    cur.close()
    return jsonify(todos)

def add_todo():
    data = request.json
    cur = current_app.config['conn'].cursor()
    cur.execute('INSERT INTO todos (text, done) VALUES (%s, %s) RETURNING id', (data['text'], False))
    todo_id = cur.fetchone()[0]
    current_app.config['conn'].commit()
    cur.close()
    return jsonify({'id': todo_id, 'text': data['text'], 'done': False}), 201

def update_todo(todo_id):
    data = request.json
    cur = current_app.config['conn'].cursor()
    cur.execute('UPDATE todos SET done = %s WHERE id = %s', (data['done'], todo_id))
    current_app.config['conn'].commit()
    cur.close()
    return jsonify({'id': todo_id, 'done': data['done']})

def metrics():
    # Example Prometheus metrics endpoint
    return 'todo_count %d\n' % get_todo_count(), 200, {'Content-Type': 'text/plain'}

def get_todo_count():
    cur = current_app.config['conn'].cursor()
    cur.execute('SELECT COUNT(*) FROM todos')
    count = cur.fetchone()[0]
    cur.close()
    return count


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
