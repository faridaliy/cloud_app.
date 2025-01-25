from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpassword@mysql/users_db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'brad'  # Required for Flask-Login


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'register'


from app import routes
