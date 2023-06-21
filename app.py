import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_json import FlaskJSON

from db import mysql
from model import main_route

load_dotenv()

app = Flask(
    __name__, static_folder="C:/Users/User/Desktop/login_test/venv/static/img"
)
CORS(app)
FlaskJSON(app)
app.config["DEBUG"] = True
app.secret_key = "r@nd0mSk_1"

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")


app.config["MYSQL_HOST"] = db_host
app.config["MYSQL_USER"] = db_user
app.config["MYSQL_PASSWORD"] = db_password
app.config["MYSQL_DB"] = db_name
app.config["MYSQL_PORT"]= int(db_port)
app.config["MYSQL_DB"] = db_name
app.register_blueprint(main_route)

if __name__ == "__main__":
    mysql.init_app(app)
    app.run(debug=True)
