from flask import Flask
from dotenv import load_dotenv
import schedule, time
import threading
from flask_cors import CORS
import signal
import sys

from router.route import api
from database.controller import delete_expired_todos

load_dotenv()

app = Flask(__name__)
app.register_blueprint(api)
CORS(app)


if __name__ == '__main__':
	# 日付が過ぎたtodoを00:00に削除する関数
	def monitoring_expired_todos():
		schedule.every().day.at("00:00").do(delete_expired_todos),
		while True:
			schedule.run_pending()
			time.sleep(1)
	# 別スレッドで実行
	monitoring_expired_todos_thread = threading.Thread(target=monitoring_expired_todos)
	monitoring_expired_todos_thread.start()

	# スレッドをjoinして終了するハンドラを生成する関数
	def signit_handler(thread: threading.Thread):
		def handler():
			thread.join()
			sys.exit(0)
		return handler

	signal.signal(signal.SIGINT, signit_handler(monitoring_expired_todos_thread))
	
	# Webアプリを実行
	app.run()