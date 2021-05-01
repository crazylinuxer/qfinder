import os
import json
from datetime import datetime, timedelta, timezone

from flask import Flask
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies

from utils import config


app = Flask(__name__)

with open(os.path.join(app.root_path, '../config.json'), 'r') as config_file:
    app.config.update(json.loads(config_file.read()))

app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY'] = app.config['JWT_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_TEMPLATE.format(
    'orgfeed_user', app.config["PGPASSWORD"], 'orgfeed_db'
)


@app.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(seconds=app.config["JWT_ACCESS_TOKEN_EXPIRES"]))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
