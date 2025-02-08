from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Surah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name_arabic = db.Column(db.String(100), nullable=False)
    name_persian = db.Column(db.String(100), nullable=False)
    revelation_type = db.Column(db.String(20))  # مکی یا مدنی
    verses_count = db.Column(db.Integer)
    verses = db.relationship('Verse', backref='surah', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Verse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    text_arabic = db.Column(db.Text, nullable=False)
    text_persian = db.Column(db.Text, nullable=False)
    audio_url = db.Column(db.String(255))
    page = db.Column(db.Integer)
    juz = db.Column(db.Integer)
    hizb = db.Column(db.Integer)
    surah_id = db.Column(db.Integer, db.ForeignKey('surah.id'), nullable=False)
    bookmarks = db.relationship('Bookmark', backref='verse', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verse_id = db.Column(db.Integer, db.ForeignKey('verse.id'), nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
