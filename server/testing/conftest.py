import pytest
from app import app, db
from models import Episode, Guest, Appearance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Create test data
            episode1 = Episode(date="1/11/99", number=1)
            episode2 = Episode(date="1/12/99", number=2)
            guest1 = Guest(name="Test Guest 1", occupation="actor")
            guest2 = Guest(name="Test Guest 2", occupation="comedian")
            
            db.session.add_all([episode1, episode2, guest1, guest2])
            db.session.commit()
            
            appearance = Appearance(rating=5, episode_id=episode1.id, guest_id=guest1.id)
            db.session.add(appearance)
            db.session.commit()
            
        yield client
        
        with app.app_context():
            db.drop_all()