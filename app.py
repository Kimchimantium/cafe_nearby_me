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

# TODO
# <small> to each index.html form labels ✓
# check whether Chrome validator works or flask-wtf validator works ✓
# make sqlalchemy save the API results + user added info
# make an add button in index.html that moves the API searched item to my list ✓
# make navigator to move to my coffee list page
# make eventlistener to show map when place clicked ✓
# disable the screen to go to top whenever plus icon is clicked ✓
# CSRF token

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
    name = db.Column(db.String(50), nullable=False)
    rating = db.column(db.String(30))
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
    location = StringField(label='Where to Search',
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
    location, result = None, []
    # Get Form Data
    results, result_names, result_emojis, result_vicinities, results_zipped = [], [], [], [], []
    if form.validate_on_submit():
        location = form.location.data
        type_ = form.type.data
        keyword = form.keyword.data
        radius = form.radius.data

        # Get Place JSON Data
        gg = GetGeo()
        result = gg.by_geo(type_=type_, keyword=keyword, address=location, radius=radius, save=True)
        results = result['results']
        for result in results:
            result_names.append(result['name'])
            result_vicinities.append(result['vicinity'])
            rating_emojis = '😶' if result['rating'] == 0 else '⭐️' * int(result['rating'])
            result_emojis.append(rating_emojis)
        results_zipped = list(zip(result_names, result_emojis, result_vicinities))

    # Get url args data
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        selected_name = data.get('name')
        selected_rating = data.get('rating')
        selected_vicinity = data.get('vicinity')
        if any(v is not None for v in [selected_name, selected_rating, selected_vicinity]):
            new_cafe = Cafe(name=selected_name,
                            rating=selected_rating,
                            map_url=f"https://www.google.com/maps/search/?api=1&query="
                                    f"{selected_name}{selected_vicinity}",
                            location=selected_vicinity
                            )
            db.session.add(new_cafe)
            db.session.commit()
    return render_template('index.html',
                           form=form,
                           location=location,
                           key=key,
                           results=results,
                           results_zipped=results_zipped)


@app.route('/find_cafes', methods=['GET'])
def find_cafes():
    pass


if __name__ == '__main__':
    app.run(port=7077, debug=True)
