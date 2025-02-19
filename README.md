# قرآن کریم

این یک برنامه وب برای مطالعه و جستجو در قرآن کریم است. با استفاده از این برنامه می‌توانید:

- سوره‌های قرآن را مطالعه کنید
- با نام فارسی سوره‌ها جستجو کنید
- آیات مورد علاقه خود را نشان‌گذاری کنید

## نصب و راه‌اندازی

1. ابتدا پروژه را کلون کنید:
```bash
git clone https://github.com/YOUR_USERNAME/quran-app.git
cd quran-app
```

2. یک محیط مجازی پایتون ایجاد کنید و آن را فعال کنید:
```bash
python -m venv venv
source venv/bin/activate  # برای لینوکس و مک
venv\Scripts\activate  # برای ویندوز
```

3. وابستگی‌ها را نصب کنید:
```bash
pip install -r requirements.txt
```

4. برنامه را اجرا کنید:
```bash
python app.py
```

5. در مرورگر خود به آدرس `http://localhost:5000` بروید.

## ویژگی‌ها

- رابط کاربری زیبا و واکنش‌گرا
- جستجوی سوره‌ها با نام فارسی
- نشان‌گذاری آیات مورد علاقه
- نمایش متن عربی و ترجمه فارسی آیات

## تکنولوژی‌ها

- Python
- Flask
- SQLite
- Bootstrap 5
- HTML/CSS/JavaScript
