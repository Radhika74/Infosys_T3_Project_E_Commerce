from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail # type: ignore

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()     #for database migration
mail = Mail()

def create_database():
    db.create_all()
    print('Database Created')



def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomstore_db.db'
    app.config['TESTING'] = True

    # RUN IN CMD OR ANY PYTHON FILE TO GENERATE A HEXADECIMAL NUMBER WHICH WE CAN USE AS A "SECRET_KEY"!!!
    # >>> import os 
    # >>> os.urandom(12).hex()
         # '3ac59e5abebccf45a46282ee'
    app.config['SECRET_KEY'] = '3ac59e5abebccf45a46282ee'

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'vishnujavvaji19@gmail.com'
    app.config['MAIL_PASSWORD'] = 'grig irqy fdob maug' #   'oowd hosw eeuv jguy'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'vishnujavvaji19@gmail.com'

    mail.init_app(app)


    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app,db)
    
    

    from .auth import auth_bp
    from .admin import admin_bp
    from .views import views_bp
    from .delivery import delivery_bp

    # from .playground import playground_bp               # ///////////////   plaground_bp    ///////////////

    app.register_blueprint(auth_bp,url_prefix="/auth")
    app.register_blueprint(admin_bp,url_prefix="/admin")
    app.register_blueprint(delivery_bp,url_prefix="/delivery")
    app.register_blueprint(views_bp,url_prefix="/")

    # app.register_blueprint(playground_bp,url_prefix="/playground")          # ///////////////   plaground    ///////////////


    # with app.app_context():
        
    #     create_database()

    
    return app



