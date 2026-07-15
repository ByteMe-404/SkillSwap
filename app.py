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
        from models.user     import User
        from models.category import Category
        from models.skill    import Skill
        from models.request  import Request
        from models.chat     import Chat
        from models.message  import Message
        from models.review   import Review
        




        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        from routes.auth        import auth_bp
        from routes.dashboard   import dashboard_bp
        from routes.profile     import profile_bp
        from routes.skills      import skills_bp
        from routes.marketplace import marketplace_bp
        from routes.requests    import requests_bp
        from routes.chat        import chat_bp
        from routes.reviews     import reviews_bp
        from routes.admin       import admin_bp


        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(profile_bp)
        app.register_blueprint(skills_bp)
        app.register_blueprint(marketplace_bp)
        app.register_blueprint(requests_bp)
        app.register_blueprint(chat_bp)
        app.register_blueprint(reviews_bp)
        app.register_blueprint(admin_bp)


    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()

    app.run(debug=True)