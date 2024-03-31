"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort, flask_admin
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Film, Starship, Vehicle, Gender, Specie, Director, Favorite
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
    body = request.get_json()  # Obtener el request body de la solicitud
    if body is None:
        return "El cuerpo de la solicitud es null", 400
    if 'first_name' not in body:
        return 'Debes especificar first_name', 400
    if 'last_name' not in body:
        return 'Debes especificar last_name', 400
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        abort(404, 'Person not found')
    return jsonify(person.to_dict()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.to_dict() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        abort(404, 'Planet not found')
    return jsonify(planet.to_dict()), 200

@app.route('/users', methods=['GET'])
def get_users():
    user = User.query.get(user_id)
    if not user:
        abort(404, 'User not found')
    return jsonify(user.to_dict()), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.get(user_id)
    if not user:
        abort(404, 'User not found')
    return jsonify([favorite.to_dict() for favorite in user.favorites]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    if not user:
        abort(404, 'User not found')
    planet = Planet.query.get(planet_id)
    if not planet:
        abort(404, 'Planet not found')
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet added successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    if not user:
        abort(404, 'User not found')
    person = People.query.get(people_id)
    if not person:
        abort(404, 'Person not found')
    favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite people added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    if not user:
        abort(404, 'User not found')
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        abort(404, 'Favorite planet not found for this user')
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite planet deleted successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    if not user:
        abort(404, 'User not found')
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        abort(404, 'Favorite people not found for this user')
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite people deleted successfully"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
