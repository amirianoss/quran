from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Surah(db.Model):
    __tablename__ = 'surahs'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name_arabic = db.Column(db.String(100), nullable=False)
    name_persian = db.Column(db.String(100), nullable=False)
    verses_count = db.Column(db.Integer, nullable=False)
    verses = db.relationship('Verse', backref='surah', lazy=True, cascade="all, delete-orphan")

class Verse(db.Model):
    __tablename__ = 'verses'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    text_arabic = db.Column(db.Text, nullable=False)
    text_persian = db.Column(db.Text, nullable=False)
    surah_id = db.Column(db.Integer, db.ForeignKey('surahs.id', ondelete='CASCADE'), nullable=False)
    bookmarks = db.relationship('Bookmark', backref='verse', lazy=True)

    @property
    def audio_url(self):
        verse_number = (self.surah.number - 1) * 1000 + self.number
        return f'https://verses.quran.com/{verse_number}.mp3'

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    verse_id = db.Column(db.Integer, db.ForeignKey('verses.id'), nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
