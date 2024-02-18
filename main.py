from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notes', lazy=True))

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    try:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Username already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/notes/create', methods=['POST'])
def create_note():
    title = request.json.get('title')
    content = request.json.get('content')
    user_id = request.json.get('user_id')
    if not title or not content or not user_id:
        return jsonify({'message': 'Title, content, and user_id are required'}), 400
    try:
        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'message': 'Note created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User does not exist'}), 404

@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    if note:
        note_schema = NoteSchema()
        return jsonify(note_schema.dump(note)), 200
    else:
        return jsonify({'message': 'Note not found'}), 404

@app.route('/notes/share', methods=['POST'])
def share_note():
    note_id = request.json.get('note_id')
    user_id = request.json.get('user_id')
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    if note.user_id == user_id:
        return jsonify({'message': 'Cannot share note with yourself'}), 400
    note.user_id = user_id
    db.session.commit()
    return jsonify({'message': 'Note shared successfully'}), 200

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    title = request.json.get('title')
    content = request.json.get('content')
    if not title and not content:
        return jsonify({'message': 'Title or content is required to update note'}), 400
    if title:
        note.title = title
    if content:
        note.content = content
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'}), 200

@app.route('/notes/version-history/<int:id>', methods=['GET'])
def get_note_version_history(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    versions = Note.query.filter_by(id=id).all()
    note_schema = NoteSchema(many=True)
    return jsonify(note_schema.dump(versions)), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
