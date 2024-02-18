# Note Taking Application API

This is a simple note-taking application API built with Flask and SQLAlchemy. It allows users to perform basic CRUD operations (Create, Read, Update, Delete) on notes.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- MySQL

## Installation

1. Clone the repository:

2. Navigate to the project directory:
    ```bash
    cd note-taking-app

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Import db schema from project directory

5. Run the application
    python main.py

## API Endpoints
- POST /signup: Create a new user account.
- POST /login: User login.
- POST /notes/create: Create a new note.
- GET /notes/{id}: Retrieve a specific note by its ID.
- POST /notes/share: Share the note with other users.
- PUT /notes/{id}: Update an existing note.
- GET /notes/version-history/{id}: Get all the changes associated with the note.

## API Testing
- Signup API:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "password": "password123"}' http://localhost:5000/signup

- Login API:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "password": "password123"}' http://localhost:5000/login

- Create Note API:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"title": "My First Note", "content": "This is the content of my first note.", "user_id": 1}' http://localhost:5000/notes/create

- Retrieve Note by ID API:
    ```bash
    curl http://localhost:5000/notes/1

- Share Note API:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"note_id": 1, "user_id": 2}' http://localhost:5000/notes/share

- Update Note API:
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"title": "Updated Title", "content": "Updated content"}' http://localhost:5000/notes/1

- Get Note Version History API:
    ```bash
    curl http://localhost:5000/notes/version-history/1
