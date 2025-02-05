import requests
from models import db, Surah, Verse
from app import app

def get_quran_data():
    # دریافت اطلاعات سوره‌ها
    surahs_response = requests.get('http://api.alquran.cloud/v1/surah')
    surahs_data = surahs_response.json()['data']
    
    with app.app_context():
        # حذف داده‌های قبلی
        db.drop_all()
        db.create_all()
        
        # افزودن سوره‌ها و آیات
        for surah_info in surahs_data:
            # دریافت اطلاعات فارسی سوره
            fa_response = requests.get(f'http://api.alquran.cloud/v1/surah/{surah_info["number"]}/fa.makarem')
            fa_data = fa_response.json()['data']
            
            # ایجاد سوره جدید
            surah = Surah(
                number=surah_info['number'],
                name_arabic=surah_info['name'],
                name_persian=fa_data['name'],
                revelation_type='مکی' if surah_info['revelationType'] == 'Meccan' else 'مدنی',
                verses_count=surah_info['numberOfAyahs']
            )
            db.session.add(surah)
            db.session.flush()  # برای دریافت id سوره
            
            # دریافت آیات عربی
            verses_response = requests.get(f'http://api.alquran.cloud/v1/surah/{surah_info["number"]}')
            verses_data = verses_response.json()['data']['ayahs']
            
            # دریافت ترجمه فارسی آیات
            verses_fa_response = requests.get(f'http://api.alquran.cloud/v1/surah/{surah_info["number"]}/fa.makarem')
            verses_fa_data = verses_fa_response.json()['data']['ayahs']
            
            print(f'در حال افزودن سوره {surah.name_persian} ({surah.number})')
            
            # افزودن آیات
            for verse_ar, verse_fa in zip(verses_data, verses_fa_data):
                verse = Verse(
                    number=verse_ar['numberInSurah'],
                    text_arabic=verse_ar['text'],
                    text_persian=verse_fa['text'],
                    audio_url=f'https://cdn.islamic.network/quran/audio/128/ar.alafasy/{verse_ar["number"]}.mp3',
                    page=verse_ar['page'],
                    juz=verse_ar['juz'],
                    hizb=verse_ar['hizbQuarter'],
                    surah_id=surah.id
                )
                db.session.add(verse)
            
            # ذخیره تغییرات هر سوره
            db.session.commit()
            print(f'سوره {surah.name_persian} با موفقیت اضافه شد')

if __name__ == '__main__':
    print('شروع دریافت و ذخیره‌سازی اطلاعات قرآن...')
    get_quran_data()
    print('اطلاعات قرآن با موفقیت در دیتابیس ذخیره شد')
