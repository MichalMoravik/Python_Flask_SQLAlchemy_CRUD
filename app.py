from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init server
app = Flask(__name__)

############ DATABASE INIT ############
# Setup sql-alchemy database URI to locate a database file
# Database file will be in a root directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///' + \
    os.path.join(basedir, 'db.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init database
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)


# Run server
if __name__ == 'main':
    app.run(debug=True)
