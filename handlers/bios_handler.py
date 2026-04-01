import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# بيانات البايوهات
WHATSAPP_BIOS = [
    "✨ الحياة بسيطة، لا تعقدها ✨", "💫 توكل على الله وتحرك 💫", "❤️ عيش حياتك بلا أسف ❤️",
    "🌙 لست متاحًا للجميع 🌙", "🔥 لا تقارنني بأحد 🔥", "🎯 راضي بقسمتي 🎯",
    "🕊️ سلام داخلي 🕊️", "⭐ تحت الإشراف الإلهي ⭐", "💎 أنا كما أنا 💎",
    "👑 ملك نفسي 👑", "🌟 القناعة كنز لا يفنى 🌟", "💪 لا مستحيل مع الإرادة 💪"
]

INSTAGRAM_BIOS = [
    "📸 | Just vibes ✨", "💫 | Living my best life", "❤️ | Love & Peace",
    "🎯 | Dream chaser", "🌙 | Night owl", "🔥 | Hustle mode",
    "🕊️ | Free soul", "⭐ | Star stuff", "💎 | Rare breed",
    "👑 | Born to shine", "🎨 | Art enthusiast", "📚 | Book lover",
    "✈️ | Travel addict", "🎵 | Music is life", "💪 | Fitness journey"
]

MESSENGER_BIOS = [
    "💬 | متاح للكلام أحيانًا", "🎮 | Gaming mode on", "📱 | Offline life online",
    "💭 | أفكار عشوائية", "🎧 | Music is life", "📚 | قراءة وكتابة",
    "🌍 | عابر سبيل", "⚡ | سريع الاستجابة", "😴 | Nap time",
    "💼 | Work mode", "🎯 | Focused", "🤝 | Open for chat"
]

def register_bios_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "bios")
    def bios_callback(call):
        """عرض قائمة البايوهات"""
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("💚 واتساب", callback_data="bio_whatsapp")
        btn2 = InlineKeyboardButton("📸 إنستجرام", callback_data="bio_instagram")
        btn3 = InlineKeyboardButton("💬 ماسنجر", callback_data="bio_messenger")
        btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="menu")
        markup.add(btn1, btn2, btn3)
        markup.add(btn4)
        
        bot.edit_message_text(
            "📝 **اختر نوع البايو:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("bio_"))
    def show_bios(call):
        """عرض البايوهات حسب النوع"""
        bio_type = call.data.split("_")[1]
        
        if bio_type == "whatsapp":
            bios = random.sample(WHATSAPP_BIOS, min(6, len(WHATSAPP_BIOS)))
            title = "💚 **بايوهات واتساب:** 💚"
        elif bio_type == "instagram":
            bios = random.sample(INSTAGRAM_BIOS, min(6, len(INSTAGRAM_BIOS)))
            title = "📸 **بايوهات إنستجرام:** 📸"
        else:
            bios = random.sample(MESSENGER_BIOS, min(6, len(MESSENGER_BIOS)))
            title = "💬 **بايوهات ماسنجر:** 💬"
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        response = title + "\n\n"
        for i, bio in enumerate(bios, 1):
            response += f"{i}️⃣ {bio}\n\n"
        
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🔄 تغيير", callback_data=f"refresh_bio_{bio_type}")
        btn2 = InlineKeyboardButton("🔙 رجوع", callback_data="bios")
        markup.add(btn1, btn2)
        
        bot.send_message(
            call.message.chat.id,
            response,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("refresh_bio_"))
    def refresh_bios(call):
        """تحديث البايوهات"""
        bio_type = call.data.split("_")[2]
        
        if bio_type == "whatsapp":
            bios = random.sample(WHATSAPP_BIOS, min(6, len(WHATSAPP_BIOS)))
            title = "💚 **بايوهات واتساب:** 💚"
        elif bio_type == "instagram":
            bios = random.sample(INSTAGRAM_BIOS, min(6, len(INSTAGRAM_BIOS)))
            title = "📸 **بايوهات إنستجرام:** 📸"
        else:
            bios = random.sample(MESSENGER_BIOS, min(6, len(MESSENGER_BIOS)))
            title = "💬 **بايوهات ماسنجر:** 💬"
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        response = title + "\n\n"
        for i, bio in enumerate(bios, 1):
            response += f"{i}️⃣ {bio}\n\n"
        
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🔄 تغيير", callback_data=f"refresh_bio_{bio_type}")
        btn2 = InlineKeyboardButton("🔙 رجوع", callback_data="bios")
        markup.add(btn1, btn2)
        
        bot.send_message(
            call.message.chat.id,
            response,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id, "✨ تم تحديث البايوهات")