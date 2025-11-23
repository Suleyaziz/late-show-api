from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os

# Initialize db first without app
db = SQLAlchemy()
migrate = Migrate()
api = Api()

# Create app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize with app
db.init_app(app)
migrate.init_app(app, db)
api.init_app(app)  # This must happen BEFORE resource registration

# Import models AFTER db is initialized
from models import Episode, Guest, Appearance

# Define your Resource classes
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

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Podcast API"})

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{
        'id': ep.id,
        'date': ep.date,
        'number': ep.number
    } for ep in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify(episode.to_dict())

@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    db.session.delete(episode)
    db.session.commit()
    return '', 204

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name,
        'occupation': g.occupation
    } for g in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        appearance = Appearance(
            rating=data.get('rating'),
            episode_id=data.get('episode_id'),
            guest_id=data.get('guest_id')
        )
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict()), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": ["Validation errors"]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)