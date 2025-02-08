from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from models import db, Surah, Verse, Bookmark

load_dotenv()

app = Flask(__name__)

# تنظیمات اولیه
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quran.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db.init_app(app)

# مسیر اصلی
@app.route('/')
def index():
    surahs = Surah.query.all()
    return render_template('index.html', surahs=surahs)

# نمایش سوره
@app.route('/surah/<int:surah_number>')
def show_surah(surah_number):
    surah = Surah.query.filter_by(number=surah_number).first_or_404()
    verses = Verse.query.filter_by(surah_id=surah.id).order_by(Verse.number).all()
    return render_template('surah.html', surah=surah, verses=verses)

# جستجو در قرآن
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # حذف کلمه "سوره" از ابتدای عبارت جستجو
    query = query.replace('سوره', '').strip()
    
    # جستجو فقط در نام فارسی سوره‌ها
    surahs = Surah.query.filter(
        Surah.name_persian.like(f'%{query}%')
    ).all()
    
    return render_template('search.html', surahs=surahs, query=query)

# نشانه‌گذاری آیه
@app.route('/bookmark/<int:verse_id>', methods=['POST', 'DELETE'])
def bookmark_verse(verse_id):
    if request.method == 'DELETE':
        bookmark = Bookmark.query.get_or_404(verse_id)
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        note = request.form.get('note', '')
        bookmark = Bookmark(verse_id=verse_id, note=note)
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({'status': 'success'})

# نمایش نشانک‌ها
@app.route('/bookmarks')
def show_bookmarks():
    bookmarks = Bookmark.query.join(Verse).join(Surah).order_by(Bookmark.created_at.desc()).all()
    return render_template('bookmarks.html', bookmarks=bookmarks)

# دریافت فایل صوتی
@app.route('/audio/<int:surah_number>/<int:verse_number>')
def get_audio(surah_number, verse_number):
    verse = Verse.query.join(Surah).filter(
        Surah.number == surah_number,
        Verse.number == verse_number
    ).first_or_404()
    return redirect(verse.audio_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
