from flask import Flask, render_template, g
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
import os
from flask_sqlalchemy import SQLAlchemy # 変更

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )
app = FlaskWithHamlish(__name__)

db_uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = "dzed"
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)

@app.route('/')
def hello_world():
    entries = Entry.query.all() #変更
    return render_template('index.haml', entries=entries)
