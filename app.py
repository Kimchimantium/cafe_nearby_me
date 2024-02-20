from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import requests
import os
from geocode import GetGeo

# ===== App Setting =====
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
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
    cafe_name = None


def create_db():
    """ Make new db """
    with app.app_context():
        db.create_all()


@app.route('/')
def home():
    key = os.getenv('GOOGLE_API_KEY')
    print(key)
    location_name = "분당"
    return render_template('index.html',
                           location_name=location_name,
                           key=key)

@app.route('/findcafes', methods=['GET'])
def find_cafes():
    print(gg.get_lat_long())
    name = request.args.get('name')
    radius = 500
    type = 'cafe'
    location = gg.get_lat_long('경기도 성남시 분당구 정자동 84-6')
    print(location)
    key = os.getenv('GOOGLE_API_KEY')
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location[0]},{location[1]}&radius={radius}&type={type}&key={key}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data from Google Places API"}), response.status_code


if __name__ == '__main__':
    app.run(port=7077, debug=True)