from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("✨ زخرفة نصوص", callback_data="decorate")
    btn2 = InlineKeyboardButton("🌍 ترجمة الأسماء", callback_data="translate")
    btn3 = InlineKeyboardButton("📝 بايوهات جاهزة", callback_data="bios")
    btn4 = InlineKeyboardButton("🎨 تأثيرات إضافية", callback_data="effects")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

def main_menu_with_admin(user_id):
    from admin.admin_handler import is_admin
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("✨ زخرفة نصوص", callback_data="decorate")
    btn2 = InlineKeyboardButton("🌍 ترجمة الأسماء", callback_data="translate")
    btn3 = InlineKeyboardButton("📝 بايوهات جاهزة", callback_data="bios")
    btn4 = InlineKeyboardButton("🎨 تأثيرات إضافية", callback_data="effects")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    if is_admin(user_id):
        btn_admin = InlineKeyboardButton("👑 لوحة التحكم", callback_data="admin_panel")
        markup.add(btn_admin)
    
    return markup

def get_more_button(name, lang):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_{lang}_{name}")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="decorate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3)
    return markup

def get_translation_more_button(name, lang):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_trans_{lang}_{name}")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="translate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3)
    return markup

def bio_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("💚 واتساب", callback_data="bio_whatsapp")
    btn2 = InlineKeyboardButton("📸 إنستجرام", callback_data="bio_instagram")
    btn3 = InlineKeyboardButton("💬 ماسنجر", callback_data="bio_messenger")
    btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3)
    markup.add(btn4)
    return markup

def effect_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📏 خط تحت", callback_data="effect_underline")
    btn2 = InlineKeyboardButton("✂️ خط وسط", callback_data="effect_strikethrough")
    btn3 = InlineKeyboardButton("🔄 نص مقلوب", callback_data="effect_reverse")
    btn4 = InlineKeyboardButton("␣ مسافات", callback_data="effect_spaces")
    btn5 = InlineKeyboardButton("📦 مربع", callback_data="effect_box")
    btn6 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def lang_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🇸🇦 عربي", callback_data="lang_arabic")
    btn2 = InlineKeyboardButton("🇬🇧 إنجليزي", callback_data="lang_english")
    markup.add(btn1, btn2)
    return markup