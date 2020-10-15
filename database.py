# database
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:password@152.3.52.135/test1'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class test1(db.Model):
    __tablename__ = 'test1'
    id = db.Column('a', db.Integer(), primary_key = True)



@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    #app.run()
    print(db.session.query(test1).all())
