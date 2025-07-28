from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def home():
    return render_template('index.html')

@frontend.route('/index.html')
def index():
    return render_template('index.html')

@frontend.route('/home', endpoint='serve_index_alias')
def serve_index_alias():
    return render_template('index.html')

@frontend.route('/login.html')
def login():
    return render_template('login.html')

@frontend.route('/place.html')
def place():
    return render_template('place.html')

@frontend.route('/add_review.html')
def add_review():
    return render_template('add_review.html')

@frontend.route('/register.html')
def register():
    return render_template('register.html')

@frontend.route('/add_place.html', endpoint='add_place')
def add_place():
    return render_template('add_place.html')

@frontend.route('/add_amenity.html', endpoint='add_amenity')
def add_amenity():
    return render_template('add_amenity.html')
