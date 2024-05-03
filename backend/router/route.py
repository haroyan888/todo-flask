from flask import Blueprint, jsonify, request
import os
import datetime
import re

from database.controller import Todo, get_all_todos, get_todo, create_todo, edit_todo, delete_todo
from modules.error import InvalidError, TodoNotFound


DATABASE = os.environ.get("DATABASE_URL")

api = Blueprint('api', __name__, url_prefix="/api")


@api.route('/')
def routing_get_all_todos():
	try:
		return jsonify({'todos': get_all_todos()})
	
	except Exception as e:
		print(e)
		return jsonify({'message': 'Internal server error'}), 500


@api.route('/create', methods=["POST"])
def routing_create_todo():
	try :
		req_todo = request.json
		if not ("title" in req_todo and "description" in req_todo and  "date" in req_todo) :
			raise InvalidError("無効なデータです")
		
		if not type(req_todo["title"]) == str or not type(req_todo["description"]) == str or not type(req_todo["date"]) == str:
			raise InvalidError("データの型が無効です")
		
		if req_todo["title"] == None or req_todo["title"] == "" or req_todo["date"] == None or req_todo["date"] == "" :
			raise InvalidError("タイトルと日付は必須です")
		
		if len(req_todo["title"]) > 255:
			raise InvalidError("タイトルが長すぎます")
		
		pattern = re.compile(r'\d{4}/\d{2}/\d{2}$')
		if pattern.match(req_todo["date"]) == None:
			raise InvalidError("日付のフォーマットが無効です")
		
		date_str = list(map(int, req_todo["date"].split("/")))
		date = datetime.datetime(date_str[0], date_str[1], date_str[2])
		
		create_todo(
			req_todo["title"],
			req_todo["description"],
			date
		)

		return jsonify({
			'result': True,
			'message': 'Success!'
		})
	
	except InvalidError as e:
		return jsonify({
			'result': False,
			'message': e.args[0]
		}), 400
	
	except Exception as e:
		print(e)
		return jsonify({
			'result': False,
			'message': 'Internal server error'
		}), 500


@api.route("/edit", methods=["POST"])
def routing_edit_todo():
	try :
		req_todo = request.json
		id = req_todo["id"]
		title = req_todo["title"] if "title" in req_todo else None
		description = req_todo["description"] if "description" in req_todo else None
		done = req_todo["done"] if "done" in req_todo else None
		date = req_todo["date"] if "date" in req_todo else None

		if not ("id" in req_todo and ("title" in req_todo or "description" in req_todo or "done" in req_todo or  "date" in req_todo)) :
			raise InvalidError("無効なデータです")

		if not(
			(title is not None and type(req_todo["title"]) == str) or
			(description is not None and (type(description) == str or description == None)) or
			(date is not None and type(req_todo["date"]) == str) or
			(done is not None and type(req_todo["done"]) == bool)
		):
			raise InvalidError("データの型が無効です")
		
		if title is not None and len(title) > 255:
			raise InvalidError("タイトルが長すぎます")
		
		if date is not None :
			pattern = re.compile(r'\d{4}/\d{2}/\d{2}$')
			if pattern.match(date) == None:
				raise InvalidError("日付のフォーマットが無効です")
			
			date_str = list(map(int, date.split("/")))
			date = datetime.datetime(date_str[0], date_str[1], date_str[2])
		
		if get_todo(id) is None:
			raise TodoNotFound("指定されたTodoが見つかりません")

		edit_todo( id, title, description, done, date )

		return jsonify({
			'result': True,
			'message': 'Success!'
		}), 200
	
	except InvalidError as e:
		return jsonify({
			'result': False,
			'message': e.args[0]
		}), 400
	
	except TodoNotFound as e:
		return jsonify({
			'result': False,
			'message': e.args[0]
		}), 400
	
	except Exception as e:
		print(e)
		return jsonify({
			'result': False,
			'message': 'Internal server error'
		}), 500


@api.route("/delete", methods=["POST"])
def routing_delete_todo():
	try:
		if not "id" in request.json:
			raise InvalidError("idを指定してください")
		
		if get_todo(request.json["id"]) is None:
			raise TodoNotFound("指定されたTodoが見つかりません")

		delete_todo(request.json["id"])

		return jsonify({
			'result': True,
			"message": "Success!"
		}), 200
	
	except InvalidError as e:
		return jsonify({
			'result': False,
			'message': e.args[0]
		}), 400
	
	except TodoNotFound as e:
		return jsonify({
			'result': False,
			'message': e.args[0]
		}), 400
	
	except Exception as e:
		print(e)
		return jsonify({
			'result': False,
			"message": "Internal Server Error"
		}), 500