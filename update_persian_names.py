from app import app, db, Surah

# لیست نام‌های فارسی سوره‌ها
persian_names = {
    1: "حمد",
    2: "بقره",
    3: "آل عمران",
    4: "نساء",
    5: "مائده",
    6: "انعام",
    7: "اعراف",
    8: "انفال",
    9: "توبه",
    10: "یونس",
    11: "هود",
    12: "یوسف",
    13: "رعد",
    14: "ابراهیم",
    15: "حجر",
    16: "نحل",
    17: "اسراء",
    18: "کهف",
    19: "مریم",
    20: "طه",
    21: "انبیاء",
    22: "حج",
    23: "مؤمنون",
    24: "نور",
    25: "فرقان",
    26: "شعراء",
    27: "نمل",
    28: "قصص",
    29: "عنکبوت",
    30: "روم",
    31: "لقمان",
    32: "سجده",
    33: "احزاب",
    34: "سبأ",
    35: "فاطر",
    36: "یس",
    37: "صافات",
    38: "ص",
    39: "زمر",
    40: "غافر",
    41: "فصلت",
    42: "شوری",
    43: "زخرف",
    44: "دخان",
    45: "جاثیه",
    46: "احقاف",
    47: "محمد",
    48: "فتح",
    49: "حجرات",
    50: "ق",
    51: "ذاریات",
    52: "طور",
    53: "نجم",
    54: "قمر",
    55: "الرحمن",
    56: "واقعه",
    57: "حدید",
    58: "مجادله",
    59: "حشر",
    60: "ممتحنه",
    61: "صف",
    62: "جمعه",
    63: "منافقون",
    64: "تغابن",
    65: "طلاق",
    66: "تحریم",
    67: "ملک",
    68: "قلم",
    69: "حاقه",
    70: "معارج",
    71: "نوح",
    72: "جن",
    73: "مزمل",
    74: "مدثر",
    75: "قیامت",
    76: "انسان",
    77: "مرسلات",
    78: "نبأ",
    79: "نازعات",
    80: "عبس",
    81: "تکویر",
    82: "انفطار",
    83: "مطففین",
    84: "انشقاق",
    85: "بروج",
    86: "طارق",
    87: "اعلی",
    88: "غاشیه",
    89: "فجر",
    90: "بلد",
    91: "شمس",
    92: "لیل",
    93: "ضحی",
    94: "شرح",
    95: "تین",
    96: "علق",
    97: "قدر",
    98: "بینه",
    99: "زلزال",
    100: "عادیات",
    101: "قارعه",
    102: "تکاثر",
    103: "عصر",
    104: "همزه",
    105: "فیل",
    106: "قریش",
    107: "ماعون",
    108: "کوثر",
    109: "کافرون",
    110: "نصر",
    111: "مسد",
    112: "اخلاص",
    113: "فلق",
    114: "ناس"
}

with app.app_context():
    # به‌روزرسانی نام‌های فارسی
    for number, name in persian_names.items():
        surah = Surah.query.filter_by(number=number).first()
        if surah:
            surah.name_persian = name
    
    # ذخیره تغییرات در دیتابیس
    db.session.commit()
    print("نام‌های فارسی سوره‌ها با موفقیت به‌روزرسانی شدند.")
