import os
import sys
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DecimalField
from wtforms.validators import DataRequired

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

class NewRecordForm(FlaskForm):
    f1 = DecimalField('f1', validators=[DataRequired()])
    f2 = DecimalField('f2', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Record')

@app.route('/')
def index():
    records = Record.query.all()
    return render_template('index.html', records=records)

@app.route('/add', methods=['GET','POST'])
def add_record():
    form = NewRecordForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        f1 = form.f1.data
        f2 = form.f2.data
        category = form.category.data
        record = Record(f1=f1, f2=f2, category=category)
        print(record)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form), 400 if form.errors else 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)