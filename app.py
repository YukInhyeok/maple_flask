from flask import Flask


def create_app():
    app = Flask(__name__)

    from views import maple
    app.register_blueprint(maple, url_prefix='/maple')

    return app
