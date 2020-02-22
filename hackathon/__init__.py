# %%
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xc5!\xddk\xd7\x08\x85\x973H\x7f\xc5D}\xf5\x92ZMW\xd0g(\x01\x03'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from hackathon import routes