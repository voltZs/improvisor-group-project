from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from improvisor import app

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/controller', methods=['GET'])
def controller():
	return render_template('controller.html')

@app.route('/presenter', methods=['GET'])
def presenter():
	return render_template('presenter.html')