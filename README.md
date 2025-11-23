# Flask RESTful API — Podcast Manager

## Project Overview

A Flask RESTful API for managing podcast episodes, guests, and their appearances, featuring a rating system to evaluate guest performances.

This API provides full CRUD operations, supports many-to-many relationships, and enforces validation rules such as rating limits (1–5).

---

## Technical Stack

* **Backend:** Flask, Flask-RESTful
* **Database:** SQLite with SQLAlchemy ORM
* **Migrations:** Flask-Migrate with Alembic
* **Serialization:** SQLAlchemy-Serializer
* **Testing:** pytest

---

## Features

* Complete CRUD operations for Episodes, Guests, and Appearances
* RESTful API with proper HTTP status codes
* Many-to-many relationships between Episodes and Guests through Appearances
* Data validation (ratings restricted to 1–5)
* Database migrations
* Error handling

---

## Data Models

### Episode

* `id` (Primary Key)
* `date` (String)
* `number` (Integer)
* Relationship: has many Guests through Appearances

### Guest

* `id` (Primary Key)
* `name` (String)
* `occupation` (String)
* Relationship: has many Episodes through Appearances

### Appearance

* `id` (Primary Key)
* `rating` (Integer, 1–5)
* `episode_id` (Foreign Key)
* `guest_id` (Foreign Key)
* Relationship: belongs to Episode and Guest

---

## API Endpoints

### Episodes

**GET /episodes**
Returns all episodes with basic information (`id`, `date`, `number`).

**GET /episodes/int:id**
Returns a specific episode with nested appearances and guest details.

**DELETE /episodes/int:id**
Deletes an episode and its associated appearances (cascade delete).

### Guests

**GET /guests**
Returns all guests with basic information (`id`, `name`, `occupation`).

### Appearances

**POST /appearances**
Creates a new appearance with `rating`, `episode_id`, and `guest_id`.
Returns created appearance with nested Episode and Guest data.

---

## Installation & Setup

This project uses a Python virtual environment, SQLite database, and Flask-Migrate for schema migrations.

### Setup Instructions

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run server
flask run
```

---

## Testing

Run the test suite using pytest:

```bash
pytest
```

---

## Database

This project uses `SQLite` with a default file named `app.db`.

Migrations are handled using `Flask-Migrate` and `Alembic`.

---

## License

This project is open source and available under the MIT License.
