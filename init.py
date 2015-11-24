from flask import Flask, g

import models

DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)

@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()
	
@app.after_request
def after_request(response):
	g.db.close()
	return response
	
if __name__ == '__main__':
	app.run(debug=DEBUG, host=HOST, port=PORT)