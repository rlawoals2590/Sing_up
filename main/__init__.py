from flask import Flask
from config import Config
from . import route
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.secret_key = Config.SESSION_SECRET_KEY
app.config["PERMANENT_SESSION_LIFETIME"] = Config.SESSION_LIMIT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.ACCESS_TOKEN
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.REFRESH_TOKEN
app.config['JWT_ACCESS_COOKIE_NAME'] = Config.COOKIE_NAME
app.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies", "json", "query_string"]


jwt = JWTManager(app)

app.register_blueprint(route.main)