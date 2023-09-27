# import smtplib
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "red"

mail = Mail()


# # Set your email and password
# email = "chordograph@gmail.com"
# password = "fhbomvhlpsjzdmzo"

# # Connect to the SMTP server
# server = smtplib.SMTP("smtp.gmail.com", 587)  # Replace with your SMTP server and port

# # Enable encryption
# server.starttls()

# # Login to the server with your credentials
# server.login(email, password)

# Send your email
# ...

# Close the connection
# server.quit()

# pass1 = bcrypt.generate_password_hash("test").decode("utf-8")
# print(pass1)
# from flaskblog import routes


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.main.routes import main
    from flaskblog.posts.routes import posts
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
