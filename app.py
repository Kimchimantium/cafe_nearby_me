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
# mycafes.html: move location in table to modal
# index.html: "near-me" button
# mycafes.html: improve carousel

# ===== App Setting =====
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # set to reduce memory usage
db = SQLAlchemy(app)
Bootstrap(app)

# ===== Custom Class Instance =====
gg = GetGeo()

# SQLDB for User Cafe Save
class Cafe(db.Model):
    __tablename__ = 'Korea'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(30))
    map_url = db.Column(db.String(250), unique=True)
    location = db.Column(db.String(50), unique=True, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))
    favorite = db.Column(db.Boolean)

# Form for index.html's Cafe Search
class CafeForm(FlaskForm):
    location = StringField(label='Where to Search',
                           validators=[validators.DataRequired()],
                           render_kw={'placeholder': '경기도 성남시 분당구 정자일로 95',
                                      'class': 'form-control',
                                      'id': 'locationInput'})
    type = SelectField(label='Place Type',
                       default='cafe',
                       choices=[('restaurant', 'Restaurant'), ('cafe', 'Café'), ('bar', 'Bar'),
                                ('hospital', 'Hospital'), ('atm', 'Atm'), ('museum', 'Museum'), ('park', 'Park'),
                                ('gas_Station', 'Gas Station'), ('supermarket', 'Supermarket')],
                       render_kw={'class': 'form-control'})
    keyword = StringField(label="Place Keyword",
                          default='스타벅스',
                          render_kw={"placeholder": 'Keyword of the Place',
                                     'class': 'form-control'})
    radius = IntegerField(label='Radius in m²',
                          default=1000,
                          validators=[validators.DataRequired()],
                          render_kw={'placeholder': 'In m²',
                                     'class': 'form-control',
                                     'id': 'radiusInput'})
    submit = SubmitField(label='Find',
                         render_kw={'class': 'btn btn-starbucks-gold form-control'})


def create_db():
    """ Make new db """
    with app.app_context():
        db.create_all()

# create_db()

# Flask App
@app.route('/', methods=['GET', 'POST'])
def home():
    key = os.getenv('GOOGLE_API_KEY')
    print(key)
    # Flask Form
    form = CafeForm()
    location, result, json_received = None, [], False
    results, result_names, result_ratings, result_emojis, result_vicinities, results_zipped = [], [], [], [], [], []
    # Get Form Data
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
            result_ratings.append(result['rating'])
            rating_emojis = '😶' if result['rating'] == 0 else '⭐️' * int(result['rating'])
            result_emojis.append(rating_emojis)

        results_zipped = list(zip(result_names, result_ratings, result_emojis, result_vicinities))
    elif request.method == 'POST' and not form.validate_on_submit():
        pass
    # Get url args data
    if request.method == 'POST' and request.is_json:
        json_received = True
        data = request.get_json()
        selected_name = data.get('name')
        selected_rating = data.get('rating')
        selected_vicinity = data.get('vicinity')
        if any(v is not None for v in [selected_name, selected_rating, selected_vicinity]):
            new_cafe = Cafe(name=selected_name,
                            rating=selected_rating,
                            map_url=f"https://www.google.com/maps/search/?api=1&query="
                                    f"{selected_name}{selected_vicinity}",
                            location=selected_vicinity,
                            favorite=False
                            )
            db.session.add(new_cafe)
            db.session.commit()
    # Get SQLDB to Check Duplicity
    cafe_db = db.session.query(Cafe).all()
    return render_template('index.html',
                           form=form,
                           location=location,
                           key=key,
                           results=results,
                           results_zipped=results_zipped,
                           cafe_db=cafe_db,
                           json_received=json_received,)


@app.route('/mycafes', methods=['POST', 'GET'])
def my_cafes():
    key = os.getenv('GOOGLE_API_KEY')
    if request.method == "POST":
        new_id = request.form.get('cafe_id')
        cafe = Cafe.query.get(new_id)
        cafe.name = request.form.get('name')
        cafe.rating = request.form.get('rating')
        cafe.map_url = request.form.get('map_url')
        cafe.location = request.form.get('location')
        cafe.seats = request.form.get('seats')
        cafe.coffee_price = request.form.get('coffee_price')
        db.session.commit()

    cafe_db = db.session.query(Cafe).all()
    favorite_db = Cafe.query.filter_by(favorite=1).all()

    if request.args.get('action') == 'delete':
        id_delete = request.args.get('cafe_id')
        cafe = Cafe.query.get(id_delete)
        db.session.delete(cafe)
        db.session.commit()
        return redirect('/mycafes')
    elif request.args.get('action') == 'favorite':
        id_favorite = request.args.get('cafe_id')
        cafe = Cafe.query.get(id_favorite)
        if cafe.favorite:
            cafe.favorite = False
        else:
            cafe.favorite = True
        db.session.commit()
        return redirect('/mycafes')

    page = request.args.get('page', 1, type=int)
    per_page = 10
    paginated_cafes = Cafe.query.paginate(page=page, per_page=per_page, error_out=False)
    for cafe in paginated_cafes:
        print(cafe.location)
    return render_template('mycafes.html',
                           key=key,
                           cafe_db=cafe_db,
                           favorite_db=favorite_db,
                           paginated_cafes=paginated_cafes)


@app.route('/info')
def info():
    pass
    return render_template('info.html')



if __name__ == '__main__':
    app.run(debug=True, port=8370)
