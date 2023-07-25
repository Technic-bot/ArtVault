import sqlite3
from flask import Flask, request, Response, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['DATABASE'] = app.root_path + '/db/' + app.config['DB_NAME']
