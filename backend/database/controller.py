import secrets
import string
import sqlite3
from dotenv import load_dotenv
import os
from datetime import datetime


def get_database_url():
	load_dotenv()
	return os.environ.get("DATABASE_URL")


def gen_id(len: int):
	return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(len))


def get_all_todos():
	conn = sqlite3.connect(get_database_url())
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM todos')
	todos = cursor.fetchall()
	conn.close()
	return [{
		"id": todo[0],
		"title": todo[1],
		"description": todo[2],
		"done": todo[3],
		"date": todo[4]
	} for todo in todos]


def create_todo(title: str, description: str, date: datetime):
	conn = sqlite3.connect(get_database_url())
	cursor = conn.cursor()
	cursor.execute(
		'''
			INSERT INTO todos (id, title, description, done, date)
			VALUES (?, ?, ?, ?, ?)
		''',
		(gen_id(32), title, description, False, date))
	conn.commit()
	conn.close()


def edit_todo(id: str, title: str, description: str, done: bool, date: datetime):
	conn = sqlite3.connect(get_database_url())
	cursor = conn.cursor()
	cursor.execute(
		'''
			UPDATE todos SET title=?, description=?, done=?, date=?
			WHERE id=?
		''',
		( title, description, done, date, id )
	)
	conn.commit()
	conn.close()


def delete_todo(id: str):
	conn = sqlite3.connect(get_database_url())
	cursor = conn.cursor()
	cursor.execute(
		'''
			DELETE FROM todos WHERE id=?
		''',
		( id, )
	)
	conn.commit()
	conn.close()