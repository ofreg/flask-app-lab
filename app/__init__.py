from flask import Flask



def create_app(config_name="config"):
    app=Flask(__name__)
    app.config.from_object(config_name)

    with app.app_context():
        from . import views

        from .posts import post_bp
        from .users import users_bp
        app.register_blueprint(post_bp)
        app.register_blueprint(users_bp)
    return app