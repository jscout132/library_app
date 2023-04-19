from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from .site.routes import book_page
from config import Config
from models import ma, db, login_manager, sess
from helpers import JSONEncoder

app = Flask(__name__)
CORS(app)


Session(app)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(book_page)

app.json_encoder = JSONEncoder


app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)
sess.init_app(app)