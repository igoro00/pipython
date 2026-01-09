import os
import sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f1 = db.Column(db.Float, nullable=False)
    f2 = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    records = Record.query.all()
    return render_template('index.html', records=records)

@app.route('/add', methods=['GET'])
def add():
    return render_template('add.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)