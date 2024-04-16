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
    user = User.query.all()
    response_body = {
        'name': user.name,
        'username': user.username,
        'lastname': user.lastname,
        'suscription': user.suscription,
        'password': user.password,
        'email': user.email,
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    result = []
    for person in people:
        person_data = {
            'name': person.name,
            'gender': person.gender.type if person.gender else None,
            'specie': person.specie.languaje if person.specie else None,
            'vehicle': person.vehicle.name if person.vehicle else None,
            'height': person.height,
            'films': [film.title for film in person.film] if person.film else []
        }
        result.append(person_data)
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
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
    people = People.query.all()
    result = []
    for planet in people:
        result.append({
            'name': planet.name,
            'population': planet.population,
            'terrain': planet.terrain,
            'diameter': planet.diameter
        })
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
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted successfully"}), 200
    else:
        return jsonify({'error': 'Favorite planet not found'}), 404
    
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    favorite = Favorite(user_id=1, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite people added successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
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

@app.route('/films', methods=['GET'])
def get_films():
    films = Film.query.all()
    result = []
    for film in films:
        result.append({
            'title': film.title,
            'director': film.director.name if film.director else None,
            'release_date': film.release_date,
            'opening_crawl': film.opening_crawl
        })
    return jsonify(result), 200

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = Film.query.get(film_id)
    if film:
        result = {
            'title': film.title,
            'director': film.director.name if film.director else None,
            'release_date': film.release_date,
            'opening_crawl': film.opening_crawl
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Film not found'}), 404

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    result = []
    for starship in starships:
        result.append({
            'name': starship.name,
            'model': starship.model,
            'manufacturer': starship.manufacturer,
            'starship_class': starship.starship_class,
            'crew': starship.crew,
            'passengers': starship.passengers
        })
    return jsonify(result), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship:
        result = {
            'name': starship.name,
            'model': starship.model,
            'manufacturer': starship.manufacturer,
            'starship_class': starship.starship_class,
            'crew': starship.crew,
            'passengers': starship.passengers
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Starship not found'}), 404

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    result = []
    for vehicle in vehicles:
        result.append({
            'name': vehicle.name,
            'model': vehicle.model,
            'manufacturer': vehicle.manufacturer,
            'vehicle_class': vehicle.vehicle_class,
            'crew': vehicle.crew,
            'passengers': vehicle.passengers
        })
    return jsonify(result), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        result = {
            'name': vehicle.name,
            'model': vehicle.model,
            'manufacturer': vehicle.manufacturer,
            'vehicle_class': vehicle.vehicle_class,
            'crew': vehicle.crew,
            'passengers': vehicle.passengers
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Vehicle not found'}), 404

@app.route('/genders', methods=['GET'])
def get_genders():
    genders = Gender.query.all()
    result = []
    for gender in genders:
        result.append({
            'id': gender.id,
            'type': gender.type
        })
    return jsonify(result), 200

@app.route('/genders/<int:gender_id>', methods=['GET'])
def get_gender(gender_id):
    gender = Gender.query.get(gender_id)
    if gender:
        result = {
            'id': gender.id,
            'type': gender.type
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Gender not found'}), 404

@app.route('/species', methods=['GET'])
def get_species():
    species = Specie.query.all()
    result = []
    for specie in species:
        result.append({
            'id': specie.id,
            'language': specie.language,
            'classification': specie.classification
        })
    return jsonify(result), 200

@app.route('/species/<int:specie_id>', methods=['GET'])
def get_specie(specie_id):
    specie = Specie.query.get(specie_id)
    if specie:
        result = {
            'id': specie.id,
            'language': specie.language,
            'classification': specie.classification
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Specie not found'}), 404

@app.route('/directors', methods=['GET'])
def get_directors():
    directors = Director.query.all()
    result = []
    for director in directors:
        result.append({
            'id': director.id,
            'name': director.name
        })
    return jsonify(result), 200

@app.route('/directors/<int:director_id>', methods=['GET'])
def get_director(director_id):
    director = Director.query.get(director_id)
    if director:
        result = {
            'id': director.id,
            'name': director.name
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Director not found'}), 404
