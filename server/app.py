from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
import os

# Configure Flask app FIRST
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize extensions WITH the app
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# Define models
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    serialize_rules = ('-appearances.episode',)
    
    def __repr__(self):
        return f'<Episode {self.number} - {self.date}>'

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    serialize_rules = ('-appearances.guest',)
    
    def __repr__(self):
        return f'<Guest {self.name} - {self.occupation}>'

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    serialize_rules = ('-episode.appearances', '-guest.appearances')
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def __repr__(self):
        return f'<Appearance Episode:{self.episode_id} Guest:{self.guest_id} Rating:{self.rating}>'

# Define routes
class EpisodesResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        return make_response(
            jsonify([episode.to_dict(rules=('-appearances',)) for episode in episodes]),
            200
        )

class EpisodeByIdResource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        return make_response(jsonify(episode.to_dict()), 200)
    
    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        db.session.delete(episode)
        db.session.commit()
        return make_response('', 204)

class GuestsResource(Resource):
    def get(self):
        guests = Guest.query.all()
        return make_response(
            jsonify([guest.to_dict(rules=('-appearances',)) for guest in guests]),
            200
        )

class AppearancesResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            appearance = Appearance(
                rating=data.get('rating'),
                episode_id=data.get('episode_id'),
                guest_id=data.get('guest_id')
            )
            db.session.add(appearance)
            db.session.commit()
            return make_response(jsonify(appearance.to_dict()), 201)
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)
        except Exception as e:
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)

# Add routes
api.add_resource(EpisodesResource, '/episodes')
api.add_resource(EpisodeByIdResource, '/episodes/<int:id>')
api.add_resource(GuestsResource, '/guests')
api.add_resource(AppearancesResource, '/appearances')

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Podcast API"})

if __name__ == '__main__':
    app.run(port=5555, debug=True)