from werkzeug.datastructures import Headers
from flask import request, Response

from apis import cors_headers
# from pages import bind_frontend_pages
from pages.errors import bind_error_pages
from repository import db
from app_creator import app
from app_creator.admin import create_admin_page
from apis import api


app.register_blueprint(api.blueprint, url_prefix='/api/v1')

# os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
# app.config["MAX_CONTENT_PATH"] = app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 5

# bind_frontend_pages(app)
bind_error_pages(app)
create_admin_page(app)

# scheduler = BackgroundScheduler()
# scheduler.add_job(post_repository.archive_expired_posts, 'cron', hour=2, max_instances=1, replace_existing=True)
# scheduler.start()
# atexit.register(scheduler.shutdown)


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


if __name__ == "__main__":
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3#600 * 1000000
    app.run(debug=True, host='0.0.0.0', port=5000)
