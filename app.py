from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, URLField, IntegerField, TimeField, SelectField
import requests
import os
from geocode import GetGeo
from pprint import pprint

# ===== App Setting =====
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # set to reduce memory usage
db = SQLAlchemy(app)
Bootstrap(app)

# ===== Custom Class Instance =====
gg = GetGeo()


class Cafe(db.Model):
    __tablename__ = 'Korea'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    map_url = db.Column(db.String(250), unique=True)
    img_url = db.Column(db.String(250), unique=True)
    location = db.Column(db.String(50), unique=True, nullable=False)
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))


class CafeForm(FlaskForm):
    location = StringField(label='Where do You Live?',
                           validators=[validators.DataRequired()],
                           render_kw={'placeholder': '경기도 성남시 분당구 정자일로 95',
                                      'class': 'form-control'})
    type = SelectField(label='Place Type',
                       default='cafe',
                       validators=[validators.DataRequired()],
                       choices=[('restaurant', 'Restaurant'), ('cafe', 'Café'), ('bar', 'Bar'),
                                ('hospital', 'Hospital'), ('atm', 'Atm'), ('museum', 'Museum'), ('park', 'Park'),
                                ('gas_Station', 'Gas Station'), ('supermarket', 'Supermarket')],
                       render_kw={'class': 'form-control'})
    keyword = StringField(label="Place Keyword",
                          default='메가커피',
                          render_kw={"placeholder": 'Keyword of the Place',
                                     'class': 'form-control'})
    radius = IntegerField(label='Radius in m²',
                          default=1000,
                          validators=[validators.DataRequired()],
                          render_kw={'placeholder': 'In m²',
                                     'class': 'form-control'})
    submit = SubmitField(label='Find',
                         render_kw={'class': 'btn btn-warning form-control'})


def create_db():
    """ Make new db """
    with app.app_context():
        db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    key = os.getenv('GOOGLE_API_KEY')

    # Flask Form
    form = CafeForm()
    location, key, result = None, None, []
    if form.validate_on_submit():
        location = form.location.data
        type_ = form.type.data
        keyword = form.keyword.data
        radius = form.radius.data
        print(f"{location}, {type_}, {keyword}, {radius}")
        gg = GetGeo()
        result = gg.by_geo(type_=type_, keyword=keyword, address=location, radius=radius, save=True)
        results = result['results']
        print(f"result: {result}")
        for result in results:
            pprint(result['rating'])
    return render_template('index.html',
                           form=form,
                           location=location,
                           key=key,
                           results=results)


@app.route('/find_cafes', methods=['GET'])
def find_cafes():
    pass


if __name__ == '__main__':
    app.run(port=7077, debug=True)
