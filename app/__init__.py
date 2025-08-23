from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.friends.routes import friends_bp
    app.register_blueprint(friends_bp)

    from app.messages.routes import messages_bp
    app.register_blueprint(messages_bp)

    from app.groups.routes import groups_bp
    app.register_blueprint(groups_bp)

    from app.posts.routes import posts_bp
    app.register_blueprint(posts_bp)

    from app.notifications.routes import notifications_bp
    app.register_blueprint(notifications_bp)

    from app.profile.routes import profile_bp
    app.register_blueprint(profile_bp, url_prefix="/profile")

    from app.admin import init_admin
    init_admin(app, db)


    return app
