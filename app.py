from flask import Flask
from config import Config
from extensions import db, login_manager, migrate 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db) 

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    with app.app_context():
        from models.user import User
        from routes.auth import auth_bp
        from routes.dashboard import dashboard_bp



        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()

    app.run(debug=True)