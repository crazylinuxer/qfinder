import os
import json
from datetime import datetime, timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (get_jwt, create_access_token, create_refresh_token,
                                get_jwt_identity, set_access_cookies, jwt_required)

from utils import config


app = Flask(__name__, template_folder="../templates", static_folder="../static")

with open(os.path.join(app.root_path, '../config.json'), 'r') as config_file:
    app.config.update(json.loads(config_file.read()))

app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY'] = app.config['JWT_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_TEMPLATE.format(
    'qfinder_user', app.config["PGPASSWORD"], 'qfinder_db'
)

jwt_manager = JWTManager(app)
