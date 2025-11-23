import pytest
from server.models import Episode, Guest, Appearance
from server.app import db

def test_episode_creation(client):
    with client.application.app_context():
        episode = Episode(date="1/15/99", number=5)
        db.session.add(episode)
        db.session.commit()
        
        assert episode.id is not None
        assert episode.date == "1/15/99"
        assert episode.number == 5

def test_guest_creation(client):
    with client.application.app_context():
        guest = Guest(name="Test Guest", occupation="writer")
        db.session.add(guest)
        db.session.commit()
        
        assert guest.id is not None
        assert guest.name == "Test Guest"
        assert guest.occupation == "writer"

def test_appearance_creation(client):
    with client.application.app_context():
        episode = Episode(date="1/16/99", number=6)
        guest = Guest(name="Test Guest 3", occupation="director")
        db.session.add_all([episode, guest])
        db.session.commit()
        
        appearance = Appearance(rating=4, episode_id=episode.id, guest_id=guest.id)
        db.session.add(appearance)
        db.session.commit()
        
        assert appearance.id is not None
        assert appearance.rating == 4
        assert appearance.episode_id == episode.id
        assert appearance.guest_id == guest.id

def test_appearance_rating_validation(client):
    with client.application.app_context():
        episode = Episode.query.first()
        guest = Guest.query.first()
        
        # Test valid rating
        valid_appearance = Appearance(rating=3, episode_id=episode.id, guest_id=guest.id)
        db.session.add(valid_appearance)
        db.session.commit()
        
        # Test invalid rating
        with pytest.raises(ValueError):
            invalid_appearance = Appearance(rating=6, episode_id=episode.id, guest_id=guest.id)
            db.session.add(invalid_appearance)
            db.session.commit()

def test_cascade_delete(client):
    with client.application.app_context():
        episode = Episode.query.first()
        episode_id = episode.id
        
        # Count appearances before delete
        appearances_before = Appearance.query.filter_by(episode_id=episode_id).count()
        assert appearances_before > 0
        
        # Delete episode
        db.session.delete(episode)
        db.session.commit()
        
        # Check if appearances were cascade deleted
        appearances_after = Appearance.query.filter_by(episode_id=episode_id).count()
        assert appearances_after == 0