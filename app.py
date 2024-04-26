from flask import Flask

def create_app():
    app = Flask(__name__)

    from views import maple  # views.py에서 maple 블루프린트를 직접 임포트합니다.
    app.register_blueprint(maple, url_prefix='/maple')  # maple 블루프린트를 등록합니다.

    return app
