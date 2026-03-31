from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    """القائمة الرئيسية"""
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("✨ زخرفة نصوص", callback_data="decorate")
    btn2 = InlineKeyboardButton("🌍 ترجمة الأسماء", callback_data="translate")
    btn3 = InlineKeyboardButton("📝 بايوهات جاهزة", callback_data="bios")
    btn4 = InlineKeyboardButton("🎨 تأثيرات إضافية", callback_data="effects")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

def translation_menu():
    """قائمة لغات الترجمة"""
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🇰🇷 كوري", callback_data="trans_korean")
    btn2 = InlineKeyboardButton("🇨🇳 صيني", callback_data="trans_chinese")
    btn3 = InlineKeyboardButton("𓂀 فرعوني", callback_data="trans_egyptian")
    btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    markup.add(btn4)
    return markup

def get_translation_more_button(name, lang):
    """أزرار المزيد للترجمة"""
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_trans_{lang}")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="translate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    return markup

def get_more_button(name, lang):
    """أزرار المزيد للزخرفة"""
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_{lang}_{name}")
    btn2 = InlineKeyboardButton("🔄 اسم جديد", callback_data="new_name")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    return markup

def bio_menu():
    """قائمة البايوهات"""
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("💚 واتساب", callback_data="bio_whatsapp")
    btn2 = InlineKeyboardButton("📸 إنستجرام", callback_data="bio_instagram")
    btn3 = InlineKeyboardButton("💬 ماسنجر", callback_data="bio_messenger")
    btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    markup.add(btn4)
    return markup

def effect_menu():
    """قائمة التأثيرات"""
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📏 خط تحت", callback_data="effect_underline")
    btn2 = InlineKeyboardButton("✂️ خط وسط", callback_data="effect_strikethrough")
    btn3 = InlineKeyboardButton("🔄 نص مقلوب", callback_data="effect_reverse")
    btn4 = InlineKeyboardButton("␣ مسافات", callback_data="effect_spaces")
    btn5 = InlineKeyboardButton("📦 مربع", callback_data="effect_box")
    btn6 = InlineKeyboardButton("🔙 رجوع", callback_data="menu")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup