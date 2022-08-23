from flask import Flask
from threading import Thread
app = Flask('')

user = None

@app.route('/')
def home():
	return f"""
	I am now running in your server as OwenTheBot#2365! :)
	This is just a web page :)
	"""

def run():
	from waitress import serve
	serve(app, host = '0.0.0.0', port = 8080)

def keep_alive():
    t = Thread(target = run)
    t.start()