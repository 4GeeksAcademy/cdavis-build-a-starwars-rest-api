from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    suscription_dates = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    favorites = db.Column(db.String(250))

class People(db.Model):
     __tablename__ = 'People'
     character_id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(250))
     gender_id = db.Column(db.Integer, db.ForeignKey('Gender.gender_id'))
     gender = db.relationship('Gender')
     specie_id = db.Column(db.Integer, db.ForeignKey('Specie.specie_id'))
     specie = db.relationship('Specie')
     vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicle.vehicle_id'))
     vehicle = db.relationship('Vehicle')
     height = db.Column(db.Integer)
     film_id = db.Column(db.Integer, db.ForeignKey('Film.film_id'))
     film = db.relationship('Film')
     planet_id = db.Column(db.Integer, db.ForeignKey('Planet.planet_id'))
     planet = db.relationship('Planet')

class Film(db.Model):
     __tablename__ = 'Film'
     film_id = db.Column(db.Integer, primary_key=True)
     director_id = db.Column(db.Integer, db.ForeignKey('Director.directo_id'))
     title = db.Column(db.String(250))
     opening = db.Column(db.String(250))
     director = db.relationship('Director')

class Starship(db.Model):
     __tablename__ = 'Starship'
     starship_id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(250))
     pilot_id = db.Column(db.Integer, db.ForeignKey('People.character_id'))
     pilot = db.relationship('People')

class Vehicle(db.Model):
     __tablename__ = 'Vehicle'
     vehicle_id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(250))
     model = db.Column(db.String(250))

class Gender(db.Model):
     __tablename__ = 'Gender'
     gender_id = db.Column(db.Integer, primary_key=True)
     type = db.Column(db.String(250))

class Specie(db.Model):
     __tablename__ = 'Specie'
     specie_id = db.Column(db.Integer, primary_key=True)
     languaje = db.Column(db.String(250))

class Planet(db.Model):
    __tablename__ = 'Planet'
    planet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    diameter = db.Column(db.Integer)

class Director(db.Model):
     __tablename__ = 'Director'
     directo_id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(250))

class Favorite(db.Model):
    __tablename__ = 'Favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User')
    planet_id = db.Column(db.Integer, db.ForeignKey('Planet.planet_id'))
    planet = db.relationship('Planet')
    film_id = db.Column(db.Integer, db.ForeignKey('Film.film_id'))
    film = db.relationship('Film')
    


def to_dict(self):
    return {}

