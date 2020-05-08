from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from WebApp.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()




#def create_app():
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from WebApp.users.routes import users
    from WebApp.main.routes import main
    from WebApp.admin.routes import admin
    from WebApp.maint.routes import maint
    from WebApp.restApi.routes import rest_api
    #from WebApp.networks.routes import networks
    from WebApp.process_control.routes import process_control
    from WebApp.dev_ops.routes import dev_ops
    from WebApp.production.routes import production
    #from WebApp.tasks.routes import tasks
    #from WebApp.posts.routes import posts
    from WebApp.errors.handlers import errors
    #from WebApp.links.routes import links
    
    app.register_blueprint(users)
    #app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    #app.register_blueprint(links)
    app.register_blueprint(admin)
    app.register_blueprint(maint)
    app.register_blueprint(rest_api)
    #app.register_blueprint(networks)
    app.register_blueprint(process_control)
    app.register_blueprint(dev_ops)
    app.register_blueprint(production)
    #app.register_blueprint(tasks)

    return app



