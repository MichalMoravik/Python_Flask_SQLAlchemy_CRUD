from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import path
# current script name
script_name = path.basename(__file__)


# Init server
app = Flask(__name__)

############# DATABASE SETUP #############
# Setup sql-alchemy database URI to locate a database file
# Database file will be in the root directory
basedir = path.abspath(path.dirname(__file__))
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

############# INIT #############
try:
    db = SQLAlchemy(app)
    ma = Marshmallow(app)
except Exception as e:
    print(f"******* Error in {script_name}: Cannot establish DB connection *******")
    print(e)

# for attr in dir(db):
#     print(f"{attr}")

# by importing routes after the app is initialized, circular import error are avoided
from sqlalchemycrud import routes