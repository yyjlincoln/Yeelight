import flask
from flask import Flask, jsonify
from flask_cors import CORS
from apiauto import auto, r

app = Flask(__name__)

@app.route('/')
@auto()

app.run()