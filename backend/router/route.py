from flask import Blueprint, jsonify, request
import sqlite3
import os

from database.controller import gen_id
from modules.error import InvalidError


DATABASE = os.environ.get("DATABASE_URL")

route = Blueprint('/', __name__)


@route.route('/')
def get_todo():
	try:
		conn = sqlite3.connect(DATABASE)
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM todos')
		todos = cursor.fetchall()
		conn.close()

		return jsonify({'todos': todos})
	
	except Exception as e:
		print(e)
		return jsonify({'message': 'Internal server error'}, 500)



@route.route('/create', methods=["POST"])
def create_todo():
	try :
		conn = sqlite3.connect(DATABASE)
		req_todo = request.json
		if not ("title" in req_todo and "description" in req_todo and  "date" in req_todo) :
			raise InvalidError("無効なデータです")

		cursor = conn.cursor()
		cursor.execute(
			'''
				INSERT INTO todos (id, title, description, done, date)
				VALUES (?, ?, ?, ?, ?)
			''',
			(gen_id(32),
			req_todo["title"],
			req_todo["description"],
			False,
			req_todo["date"]))
		conn.commit()
		conn.close()

		return jsonify({'message': 'Todo created'})
	
	except InvalidError as e:
		return jsonify({'message': e.args[0]}, 400)
	
	except Exception as e:
		print(e)
		return jsonify({'message': 'Internal server error'}, 500)


@route.route("/edit", methods=["POST"])
def edit_todo():
	try :
		conn = sqlite3.connect(DATABASE)
		req_todo = request.json
		if not ("title" in req_todo and "description" in req_todo and  "date" in req_todo) :
			raise InvalidError("無効なデータです")

		cursor = conn.cursor()
		cursor.execute(
			'''
				UPDATE todos SET title=?, description=?, date=?, done=?
				WHERE id=?
			''',
			( req_todo["title"], req_todo["description"], req_todo["date"], req_todo["done"], req_todo["id"])
		)
		conn.commit()
		conn.close()

		return jsonify({'message': 'edit success!'})
	
	except InvalidError as e:
		return jsonify({'message': e.args[0]}, 400)
	
	except Exception as e:
		print(e)
		return jsonify({'message': 'Internal server error'}, 500)
