import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    suscription_dates = Column(String(250), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(250), nullable=False)
    favorites = Column(String(250))

class People(Base):
     __tablename__ = 'People'
     character_id = Column(Integer, primary_key=True)
     name = Column(String(250))
     gender_id = Column(Integer, ForeignKey('Gender.gender_id'))
     gender = relationship('Gender')
     specie_id = Column(Integer, ForeignKey('Specie.specie_id'))
     specie = relationship('Specie')
     vehicle_id = Column(Integer, ForeignKey('Vehicle.vehicle_id'))
     vehicle = relationship('Vehicle')
     height = Column(Integer)
     film_id = Column(Integer, ForeignKey('Film.film_id'))
     film = relationship('Film')
     planet_id = Column(Integer, ForeignKey('Planet.planet_id'))
     planet = relationship('Planet')

class Film(Base):
     __tablename__ = 'Film'
     film_id = Column(Integer, primary_key=True)
     director_id = Column(Integer, ForeignKey('Director.directo_id'))
     title = Column(String(250))
     opening = Column(String(250))
     director = relationship('Director')

class Starship(Base):
     __tablename__ = 'Starship'
     starship_id = Column(Integer, primary_key=True)
     name = Column(String(250))
     pilot_id = Column(Integer, ForeignKey('People.character_id'))
     pilot = relationship('People')

class Vehicle(Base):
     __tablename__ = 'Vehicle'
     vehicle_id = Column(Integer, primary_key=True)
     name = Column(String(250))
     model = Column(String(250))

class Gender(Base):
     __tablename__ = 'Gender'
     gender_id = Column(Integer, primary_key=True)
     type = Column(String(250))

class Specie(Base):
     __tablename__ = 'Specie'
     specie_id = Column(Integer, primary_key=True)
     languaje = Column(String(250))

class Planet(Base):
    __tablename__ = 'Planet'
    planet_id = Column(Integer, primary_key=True)
    name = Column(String(250))
    population = Column(Integer)
    terrain = Column(Integer)
    diameter = Column(Integer)

class Director(Base):
     __tablename__ = 'Director'
     directo_id = Column(Integer, primary_key=True)
     name = Column(String(250))

class Favorite(Base):
    __tablename__ = 'Favorite'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship('User')
    planet_id = Column(Integer, ForeignKey('Planet.planet_id'))
    planet = relationship('Planet')
    film_id = Column(Integer, ForeignKey('Film.film_id'))
    film = relationship('Film')


def to_dict(self):
    return {}

