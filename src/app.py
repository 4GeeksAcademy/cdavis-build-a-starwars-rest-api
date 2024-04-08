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
from models import db, User, People, Planet, Film, Starship, Vehicle, Gender, Specie, Director, Favorite
#from models import Person

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    result = []
    for person in people:
        result.append({
            'name': person.name,
            'gender': person.gender.type if person.gender else None,
            'specie': person.specie.languaje if person.specie else None,
            'vehicle': person.vehicle.name if person.vehicle else None,
            'height': person.height,
            'films': [film.title for film in person.film]
        })
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        result = {
            'name': person.name,
            'gender': person.gender.type if person.gender else None,
            'specie': person.specie.languaje if person.specie else None,
            'vehicle': person.vehicle.name if person.vehicle else None,
            'height': person.height,
            'films': [film.title for film in person.film]
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Person not found'}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    result = []
    for planet in planets:
        result.append({
            'id': planet.planet_id,
            'name': planet.name,
            'population': planet.population,
            'terrain': planet.terrain,
            'diameter': planet.diameter
        })
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        result = {
            'name': planet.name,
            'population': planet.population,
            'terrain': planet.terrain,
            'diameter': planet.diameter
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Planet not found'}), 404

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    result = []
    for favorite in favorites:
        result.append({
            'user_id': favorite.user_id,
            'planet_id': favorite.planet_id,
            'film_id': favorite.film_id
        })
    return jsonify(result), 200

@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    # Assuming you have user_id available, you can replace 'user_id' with the actual user ID
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Assuming you have user_id available, you can replace 'user_id' with the actual user ID
    favorite = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted successfully"}), 200
    else:
        return jsonify({'error': 'Favorite planet not found'}), 404
    
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # Suponiendo que tengas el ID del usuario disponible, puedes reemplazar 'user_id' con el ID de usuario real
    favorite = Favorite(user_id=1, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite people added successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Suponiendo que tengas el ID del usuario disponible, puedes reemplazar 'user_id' con el ID de usuario real
    favorite = Favorite.query.filter_by(user_id=1, people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite people deleted successfully"}), 200
    else:
        return jsonify({'error': 'Favorite people not found'}), 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
