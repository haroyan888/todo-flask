import secrets
import string
import sqlite3
from dotenv import load_dotenv
import os
from datetime import datetime


class Todo():
	id: str
	title: str
	description: str|None
	done: bool
	date: datetime

	def __init__(self, id: str, title: str, description: str|None, done: bool, date: datetime):
		self.id=id
		self.title=title
		self.description=description
		self.done=done
		self.date=date

	def to_dict(self):
		return {
			"id": self.id,
			"title": self.title,
			"description": self.description,
			"done": self.done,
			"date": self.date
		}


def get_database_url():
	load_dotenv()
	return os.environ.get("DATABASE_URL")


def gen_id(len: int):
	return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(len))


def get_todo(id: str) -> dict | None:
	conn = sqlite3.connect(get_database_url())
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM todos WHERE id = ?', (id, ))
	todo = cursor.fetchone()
	conn.close()
	
	if todo is None:
		return None
	
	return {
		"id": todo[0],
		"title": todo[1],
		"description": todo[2],
		"done": todo[3],
		"date": todo[4]
	}


def get_all_todos() -> list[dict]:
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


def edit_todo(id: str, title: str | None, description: str | None, done: bool | None, date: datetime | None):
	original_todo = get_todo(id)
	conn = sqlite3.connect(get_database_url())
	cursor = conn.cursor()
	cursor.execute(
		'''
			UPDATE todos SET title=?, description=?, done=?, date=?
			WHERE id=?
		''',
		(
			title if title is not None else original_todo["title"],
			description if description is not None else original_todo["description"],
			done if done is not None else original_todo["done"],
			date if date is not None else original_todo["date"],
			id
		)
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


def delete_expired_todos():
	conn = sqlite3.connect(get_database_url())
	cursor = conn.cursor()
	cursor.execute(
		"""
			DELETE * FROM todos WHERE date < ?
		""",
		datetime.now()
	)
	conn.commit()
	conn.close()