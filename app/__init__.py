from flask import Flask
from app.models import db
from app.ui.routes import ui_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    with app.app_context():
        from app.ui import routes
        app.register_blueprint(ui_bp)
        db.create_all()
    return app
