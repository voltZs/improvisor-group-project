from flask import Flask, render_template
from improvisor import app, socketio

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/controller', methods=['GET'])
def controller():
	return render_template('controller.html')

@app.route('/presenter', methods=['GET'])
def presenter():
	return render_template('presenter.html')