import os
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
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

@dataclass
class Record(db.Model):
    id: int
    f1: float
    f2: float
    category: str

    id = db.Column(db.Integer, primary_key=True)
    f1 = db.Column(db.Float, nullable=False)
    f2 = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    @validates("category")
    def validate_string(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f"{key} must be a string")
        
        if not value.strip():
            raise ValueError(f"{key} cannot be empty")
        return value

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

@app.route('/delete/<int:id>', methods=["POST"])
def delete_record(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/api/data', methods=['GET'])
def get_data():
    records = Record.query.all()
    return jsonify(records)

@app.route('/api/data', methods=['POST'])
def add_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        for field in ['f1', 'f2', 'category']:
            if field not in data:
                raise ValueError(f"{field} cannot be empty")
    
        record = Record(**data)
        db.session.add(record)
        db.session.commit()
        
        return jsonify({"id":record.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    record = Record.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({"id":record.id}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)