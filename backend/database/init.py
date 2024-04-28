import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE = os.environ.get("DATABASE_URL")

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute('''
	CREATE TABLE IF NOT EXISTS todos (
		id CHAR(32) PRIMARY KEY,
		title CHAR(100) NOT NULL,
		description TEXT NOT NULL,
		done BOOLEAN NOT NULL,
		date DATE NOT NULL
	)
''')
conn.commit()
conn.close()
print('Tables created successfully')