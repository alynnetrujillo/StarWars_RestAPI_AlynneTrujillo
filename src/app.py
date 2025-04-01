"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Favorite_People, Favorite_Planets 


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():

    users = User.query.all()
    serialized_users = list(map(lambda x: x.serialize(), users))

    return jsonify(serialized_users=serialized_users), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    # get all the people
    favorite_people = Favorite_People.query.all()
    favorites_planets = Favorite_Planets.query.all()

    all_favorites = favorite_people + favorites_planets

    serialized_favorites = list(map(lambda x: x.serialize(), all_favorites))

    return jsonify(serialized_favorites), 200


@app.route('/people', methods=['GET'])
def get_people():

    people = User.query.all()
    serialized_people = list(map(lambda x: x.serialize(), people))

    return jsonify(serialized_people = serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    if people_id:
        person = People.query.get(people_id)
        if person:
            return jsonify(person.serialize()), 200
        else:
            return jsonify({"msg": "Person not found"}), 404


@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planets.query.all()
    serialized_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(serialized_planets = serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    if planet_id:
        planet = Planets.query.get(planet_id)
        if planet:
            return jsonify(planet.serialize()), 200
        else:
            return jsonify({"msg": "Planet not found"}), 404
        

@app.route('/favorite/planet/<planet_id>', methods=['POST', 'DELETE'])
def favorite_planet(planet_id):
    if request.method == 'POST':
        planet = Planets.query.get(planet_id)
        if planet:
            planet.is_favorite = True
            db.session.commit()
            return jsonify({"msg": "Planet marked as favorite"}), 200
        else:
            return jsonify({"msg": "Planet not found"}), 404

    elif request.method == 'DELETE':
        planet = Planets.query.get(planet_id)
        if planet:
            planet.is_favorite = False
            db.session.commit()
            return jsonify({"msg": "Planet removed from favorites"}), 200
        else:
            return jsonify({"msg": "Planet not found"}), 404
        
@app.route('/favorite/people/<people_id>', methods=['POST', 'DELETE'])
def favorite_people(people_id):
    if request.method == 'POST':
        person = People.query.get(people_id)
        if person:
            person.is_favorite = True
            db.session.commit()
            return jsonify({"msg": "Person marked as favorite"}), 200
        else:
            return jsonify({"msg": "Person not found"}), 404

    elif request.method == 'DELETE':
        person = People.query.get(people_id)
        if person:
            person.is_favorite = False
            db.session.commit()
            return jsonify({"msg": "Person removed from favorites"}), 200
        else:
            return jsonify({"msg": "Person not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
