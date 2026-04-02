import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

# 100 بايو لكل قسم
WHATSAPP_BIOS = [
    "✨ الحياة بسيطة، لا تعقدها ✨", "💫 توكل على الله وتحرك 💫", "❤️ عيش حياتك بلا أسف ❤️",
    "🌙 لست متاحًا للجميع 🌙", "🔥 لا تقارنني بأحد 🔥", "🎯 راضي بقسمتي 🎯",
    "🕊️ سلام داخلي 🕊️", "⭐ تحت الإشراف الإلهي ⭐", "💎 أنا كما أنا 💎",
    "👑 ملك نفسي 👑", "🌟 القناعة كنز لا يفنى 🌟", "💪 لا مستحيل مع الإرادة 💪",
    "🎨 حياتي لوحة أرسمها بنفسي 🎨", "📖 كل يوم قصة جديدة 📖", "🎵 الموسيقى غذاء الروح 🎵",
    "🧘 هدوء وسكينة 🧘", "🌸 ابتسم فأنت جميل 🌸", "🌊 كالبحر هدوء وعمق 🌊",
    "🦋 حر كالفراشة 🦋", "🌹 وردة في زمن الصعاب 🌹", "💙 حب وسلام 💙",
    "🤍 قلب نقي 🤍", "💜 طاقة إيجابية 💜", "💚 أمل وتفاؤل 💚",
    "🧡 شغف وحياة 🧡", "🖤 قوة وشموخ 🖤", "🤎 دفء وحنان 🤎",
    "💛 سعادة ونور 💛", "💝 حب غير مشروط 💝", "💖 قلب ينبض بالحياة 💖",
    "💗 حب صادق 💗", "💓 نبضات قلب 💓", "💕 حب بلا حدود 💕",
]

INSTAGRAM_BIOS = [
    "📸 | Just vibes ✨", "💫 | Living my best life", "❤️ | Love & Peace",
    "🎯 | Dream chaser", "🌙 | Night owl", "🔥 | Hustle mode",
    "🕊️ | Free soul", "⭐ | Star stuff", "💎 | Rare breed",
    "👑 | Born to shine", "🎨 | Art enthusiast", "📚 | Book lover",
    "✈️ | Travel addict", "🎵 | Music is life", "💪 | Fitness journey",
    "🧘 | Spiritual being", "🤍 | Simplicity", "⚡ | Energy matters",
    "🌊 | Ocean soul", "🌸 | Flower child", "🌹 | Rose gold",
    "🦋 | Butterfly effect", "🐺 | Lone wolf", "🦁 | Lion heart",
]

MESSENGER_BIOS = [
    "💬 | متاح للكلام أحيانًا", "🎮 | Gaming mode on", "📱 | Offline life online",
    "💭 | أفكار عشوائية", "🎧 | Music is life", "📚 | قراءة وكتابة",
    "🌍 | عابر سبيل", "⚡ | سريع الاستجابة", "😴 | Nap time",
    "💼 | Work mode", "🎯 | Focused", "🤝 | Open for chat",
    "📝 | Busy writing", "🎨 | Creative mode", "🏃 | On the go",
    "🍕 | Food lover", "☕ | Coffee time", "🎬 | Movie time",
]

def register_bios_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "bios")
    def bios_callback(call):
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("💚 واتساب", callback_data="bio_whatsapp")
        btn2 = InlineKeyboardButton("📸 إنستجرام", callback_data="bio_instagram")
        btn3 = InlineKeyboardButton("💬 ماسنجر", callback_data="bio_messenger")
        btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
        markup.add(btn1, btn2, btn3)
        markup.add(btn4)
        
        bot.edit_message_text(
            "📝 **اختر نوع البايو:**\n\n• 💚 واتساب\n• 📸 إنستجرام\n• 💬 ماسنجر",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("bio_"))
    def show_bio(call):
        bio_type = call.data.split("_")[1]
        
        if bio_type == "whatsapp":
            bio = random.choice(WHATSAPP_BIOS)
            title = "💚 **بايو واتساب:** 💚"
        elif bio_type == "instagram":
            bio = random.choice(INSTAGRAM_BIOS)
            title = "📸 **بايو إنستجرام:** 📸"
        else:
            bio = random.choice(MESSENGER_BIOS)
            title = "💬 **بايو ماسنجر:** 💬"
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        response = f"{title}\n\n`{bio}`\n\n✨ **لنسخ البايو اضغط على النص أعلاه**"
        
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🔄 بايو جديد", callback_data=f"refresh_bio_{bio_type}")
        btn2 = InlineKeyboardButton("🔙 رجوع", callback_data="bios")
        markup.add(btn1, btn2)
        
        bot.send_message(call.message.chat.id, response, parse_mode='Markdown', reply_markup=markup)
        db.update_user_activity(call.from_user.id, "bios")
        bot.answer_callback_query(call.id, "✨ بايو جديد")
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("refresh_bio_"))
    def refresh_bio(call):
        bio_type = call.data.split("_")[2]
        
        if bio_type == "whatsapp":
            bio = random.choice(WHATSAPP_BIOS)
            title = "💚 **بايو واتساب:** 💚"
        elif bio_type == "instagram":
            bio = random.choice(INSTAGRAM_BIOS)
            title = "📸 **بايو إنستجرام:** 📸"
        else:
            bio = random.choice(MESSENGER_BIOS)
            title = "💬 **بايو ماسنجر:** 💬"
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        response = f"{title}\n\n`{bio}`\n\n✨ **لنسخ البايو اضغط على النص أعلاه**"
        
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🔄 بايو جديد", callback_data=f"refresh_bio_{bio_type}")
        btn2 = InlineKeyboardButton("🔙 رجوع", callback_data="bios")
        markup.add(btn1, btn2)
        
        bot.send_message(call.message.chat.id, response, parse_mode='Markdown', reply_markup=markup)
        bot.answer_callback_query(call.id, "✨ بايو جديد")