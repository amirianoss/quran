from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
import os
from models import db, Surah, Verse, Bookmark
import requests

app = Flask(__name__)

# تنظیمات اولیه
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quran.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# مسیر اصلی
@app.route('/')
def index():
    surahs = Surah.query.order_by(Surah.number).all()
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
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html', surahs=[], verses=[], query='')

    # حذف کلمه "سوره" از ابتدای عبارت جستجو
    clean_query = query.replace('سوره', '').strip()
    print(f"Clean Query: {clean_query}")  # لاگ برای دیباگ
    
    # جستجو در سوره‌ها
    surahs = Surah.query.filter(
        db.or_(
            Surah.name_persian.ilike(f'%{clean_query}%'),
            Surah.name_arabic.ilike(f'%{clean_query}%')
        )
    ).all()
    print(f"Found {len(surahs)} surahs")  # لاگ برای دیباگ
    
    # جستجو در آیات
    verses = Verse.query.filter(
        db.or_(
            Verse.text_persian.ilike(f'%{query}%'),
            Verse.text_arabic.ilike(f'%{query}%')
        )
    ).order_by(Verse.surah_id, Verse.number).all()
    print(f"Found {len(verses)} verses")  # لاگ برای دیباگ

    # چاپ نام همه سوره‌ها برای دیباگ
    all_surahs = Surah.query.all()
    print("All surahs in database:")
    for surah in all_surahs:
        print(f"- {surah.number}: {surah.name_persian} ({surah.name_arabic})")

    return render_template('search.html', surahs=surahs, verses=verses, query=query)

# نمایش نشانک‌ها
@app.route('/bookmarks')
def bookmarks():
    all_bookmarks = Bookmark.query.order_by(Bookmark.created_at.desc()).all()
    return render_template('bookmarks.html', bookmarks=all_bookmarks)

# افزودن نشانک
@app.route('/bookmark/add', methods=['POST'])
def add_bookmark():
    verse_id = request.form.get('verse_id')
    note = request.form.get('note', '')

    if not verse_id:
        return jsonify({'status': 'error', 'message': 'شناسه آیه الزامی است'}), 400

    verse = Verse.query.get(verse_id)
    if not verse:
        return jsonify({'status': 'error', 'message': 'آیه مورد نظر یافت نشد'}), 404

    bookmark = Bookmark(verse_id=verse_id, note=note)
    db.session.add(bookmark)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'نشانک با موفقیت اضافه شد'})

# حذف نشانک
@app.route('/bookmark/delete/<int:bookmark_id>', methods=['POST'])
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    db.session.delete(bookmark)
    db.session.commit()
    return redirect(url_for('bookmarks'))

# دریافت فایل صوتی
@app.route('/audio/<int:surah_number>/<int:verse_number>')
def get_audio(surah_number, verse_number):
    verse_number_total = (surah_number - 1) * 1000 + verse_number
    audio_url = f'https://verses.quran.com/{verse_number_total}.mp3'
    response = requests.get(audio_url, verify=False)
    if response.status_code == 200:
        return response.content, 200, {'Content-Type': 'audio/mpeg'}
    else:
        return '', 404

if __name__ == '__main__':
    app.run(debug=True)
