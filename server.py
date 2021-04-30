import os
import json

from flask import Flask, request, Response
from werkzeug.datastructures import Headers

from apis import api, cors_headers
from frontend_bindings.pages import bind_frontend_pages
from frontend_bindings.errors import bind_error_pages
from repositories import db, post_repository
from utils import config

app = Flask(__name__)
app.register_blueprint(api.blueprint, url_prefix='/api/v1')


with open(os.path.join(app.root_path, 'config.json'), 'r') as config_file:
    app.config.update(json.loads(config_file.read()))

app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY'] = app.config['JWT_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_TEMPLATE.format(
    'orgfeed_user', app.config["PGPASSWORD"], 'orgfeed_db'
)

# os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
# app.config["MAX_CONTENT_PATH"] = app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 5


bind_frontend_pages(app)
bind_error_pages(app)


@app.after_request
def after_request(response: Response):
    db.session.rollback()

    headers = dict(response.headers)
    headers["Cache-Control"] = "no-transform"
    headers.update(**cors_headers)
    response.headers = Headers(headers)

    path = request.path
    if path.startswith("/api/v") and path.endswith("/") and path.count("/") == 3:
        body = response.get_data().replace(b"<head>", b"<head><style>.models {display: none !important}</style>")
        return Response(body, response.status_code, response.headers)
    return response


# scheduler = BackgroundScheduler()
# scheduler.add_job(post_repository.archive_expired_posts, 'cron', hour=2, max_instances=1, replace_existing=True)
# scheduler.start()
# atexit.register(scheduler.shutdown)


if __name__ == "__main__":
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 * 1000000
    app.run(debug=True, host='0.0.0.0', port=5000)
