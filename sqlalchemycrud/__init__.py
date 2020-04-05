# this is where I initialize my application and components
###################################################
from flask import Flask
# SQLAlchemy provides SQL syntax in Python
from flask_sqlalchemy import SQLAlchemy
# Marshmallow converts complex datatypes, such as objects, to and from native Python datatypes.
from flask_marshmallow import Marshmallow
import os

# Init server
app = Flask(__name__)

############# DATABASE #############
# Setup sql-alchemy database URI to locate a database file
# Database file will be in a root directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init database
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)

# for attr in dir(db):
#     print(f"{attr}")


# import after the "app" is setup so I do not run into circular imports error
from sqlalchemycrud import routes