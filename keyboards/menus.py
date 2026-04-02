from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from admin.admin_handler import is_admin

def main_menu(user_id):
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