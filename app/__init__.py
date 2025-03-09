from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail

db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()

def create_database():
    db.create_all()
    print('Database Created')



def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomstore_db.db'


    # RUN IN CMD OR ANY PYTHON FILE TO GENERATE A HEXADECIMAL NUMBER WHICH WE CAN USE AS A "SECRET_KEY"!!!
    # >>> import os 
    # >>> os.urandom(12).hex()
         # '3ac59e5abebccf45a46282ee'
    app.config['SECRET_KEY'] = '3ac59e5abebccf45a46282ee'
    db.init_app(app)
    csrf.init_app(app)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'vishnujavvaji19@gmail.com'
    app.config['MAIL_PASSWORD'] = 'grig irqy fdob maug' #   'oowd hosw eeuv jguy'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'vishnujavvaji19@gmail.com'

    mail.init_app(app)
    

    from .auth import auth_bp
    from .admin import admin_bp
    from .views import views_bp

    app.register_blueprint(auth_bp,url_prefix="/auth")
    app.register_blueprint(admin_bp,url_prefix="/admin")
    app.register_blueprint(views_bp,url_prefix="/")


    with app.app_context():
        
         create_database()

    
    return app



