from flask import Blueprint, jsonify, request
import os
import datetime
import re

from database.controller import get_all_todos, create_todo, edit_todo, delete_todo
from modules.error import InvalidError


DATABASE = os.environ.get("DATABASE_URL")

route = Blueprint('/', __name__)


@route.route('/')
def routing_get_all_todos():
	try:
		return jsonify({'todos': get_all_todos()})
	
	except Exception as e:
		print(e)
		return jsonify({'message': 'Internal server error'}), 500


@route.route('/create', methods=["POST"])
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

		return jsonify({'message': 'Success!'})
	
	except InvalidError as e:
		return jsonify({'message': e.args[0]}), 400
	
	except Exception as e:
		print(e)
		return jsonify({'message': 'Internal server error'}), 500


@route.route("/edit", methods=["POST"])
def routing_edit_todo():
	try :
		req_todo = request.json
		if not ("title" in req_todo and "description" in req_todo and  "date" in req_todo) :
			raise InvalidError("無効なデータです")
		
		if not(type(req_todo["title"]) == str and type(req_todo["description"]) == str and type(req_todo["date"]) == str and type(req_todo["done"] == bool)):
			raise InvalidError("データの型が無効です")
		
		if len(req_todo["title"]) > 255:
			raise InvalidError("タイトルが長すぎます")
		
		pattern = re.compile(r'\d{4}/\d{2}/\d{2}$')
		if pattern.match(req_todo["date"]) == None:
			raise InvalidError("日付のフォーマットが無効です")
		
		date_str = list(map(int, req_todo["date"].split("/")))
		date = datetime.datetime(date_str[0], date_str[1], date_str[2])

		edit_todo( request.args.get("id"), req_todo["title"], req_todo["description"], req_todo["done"], date )

		return jsonify({'message': 'Success!'}), 200
	
	except InvalidError as e:
		return jsonify({'message': e.args[0]}), 400
	
	except Exception as e:
		print(e)
		return jsonify({'message': 'Internal server error'}), 500


@route.route("/delete")
def routing_delete_todo():
	try:
		delete_todo(request.args.get("id"))

		return jsonify({"message": "Success!"}), 200
	
	except Exception as e:
		print(e)
		return jsonify({"message": "Internal Server Error"}), 500