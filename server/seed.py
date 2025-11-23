from app import app, db
from models import Episode, Guest, Appearance

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create episodes
        episodes = [
            Episode(date="1/11/99", number=1),
            Episode(date="1/12/99", number=2),
            Episode(date="1/13/99", number=3),
            Episode(date="1/14/99", number=4),
        ]

        # Create guests
        guests = [
            Guest(name="Michael J. Fox", occupation="actor"),
            Guest(name="Sandra Bernhard", occupation="Comedian"),
            Guest(name="Tracey Ullman", occupation="television actress"),
            Guest(name="Robin Williams", occupation="actor"),
        ]

        # Add to session
        db.session.add_all(episodes)
        db.session.add_all(guests)
        db.session.commit()

        # Create appearances
        appearances = [
            Appearance(rating=4, episode_id=1, guest_id=1),
            Appearance(rating=5, episode_id=1, guest_id=2),
            Appearance(rating=3, episode_id=2, guest_id=3),
            Appearance(rating=5, episode_id=2, guest_id=4),
            Appearance(rating=4, episode_id=3, guest_id=1),
            Appearance(rating=2, episode_id=4, guest_id=2),
        ]

        db.session.add_all(appearances)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()