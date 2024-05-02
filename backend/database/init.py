import sqlite3

from database.controller import get_database_url


conn = sqlite3.connect(get_database_url)
cursor = conn.cursor()
cursor.execute('''
	CREATE TABLE IF NOT EXISTS todos (
		id CHAR(32) PRIMARY KEY,
		title CHAR(255) NOT NULL,
		description TEXT,
		done BOOLEAN NOT NULL,
		date DATE NOT NULL
	)
''')
conn.commit()
conn.close()

print('Tables created successfully')