from flask import Flask
from dotenv import load_dotenv

from router.route import route

load_dotenv()

app = Flask(__name__)

app.register_blueprint(route)

if __name__ == '__main__':
	app.run()