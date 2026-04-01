import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============= 200 بايو واتساب =============
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
    "💞 قصة حب 💞", "💘 سهم الحب 💘", "💌 رسالة حب 💌",
    "🎭 حياتي مسرحية 🎭", "🎪 عجلة الحياة 🎪", "🎡 فرح وسعادة 🎡",
    "🎢 مغامرات الحياة 🎢", "🎠 أحلام وردية 🎠", "🏰 مملكتي الخاصة 🏰",
    "🏝️ جزيرة الهدوء 🏝️", "🏔️ قمة الطموح 🏔️", "🌋 شغف لا ينطفئ 🌋",
    "🌈 قوس قزح حياتي 🌈", "🌅 فجر جديد 🌅", "🌄 غروب جميل 🌄",
    "🌌 كون واسع 🌌", "🌠 أمنية تتحقق 🌠", "🎇 أفراح وأحلام 🎇",
    "🎆 ليلة سعيدة 🎆", "🌃 ليالي هانئة 🌃", "🌁 ضباب الأحلام 🌁",
    "🌉 جسر الأمل 🌉", "🌊 موج الحياة 🌊", "🍃 نسمات رقيقة 🍃",
    "🍂 خريف العمر 🍂", "🌸 ربيع الحياة 🌸", "☀️ شمس الأمل ☀️",
    "🌙 قمر الليالي 🌙", "⭐ نجمي الخاص ⭐", "☁️ سحابة هادئة ☁️",
    "⛈️ عاصفة إيجابية ⛈️", "❄️ ثلج الصفاء ❄️", "🔥 حماس وشغف 🔥",
    "⚡ طاقة لا تقهر ⚡", "💨 حرية واندفاع 💨", "💧 صفاء ونقاء 💧",
    "🍀 حظ سعيد 🍀", "🎋 أماني تتحقق 🎋", "🎍 تفاؤل وأمل 🎍",
    "🎑 مناظر جميلة 🎑", "🎇 أضواء الحياة 🎇", "🎆 أفراح وأحلام 🎆",
    "🎊 مناسبات سعيدة 🎊", "🎉 أفراح وأعياد 🎉", "🎈 مرح وفرح 🎈",
    "🎁 هدية الحياة 🎁", "🎀 لمسة أنثوية 🎀", "🎓 شهادة نجاح 🎓",
    "🏆 إنجازاتي 🏆", "🥇 الأول دائماً 🥇", "🥈 الهدف القادم 🥈",
    "🥉 خطوات النجاح 🥉", "🏅 إنجاز جديد 🏅", "🎖️ تكريم وتقدير 🎖️",
    "🏆 بطل حياتي 🏆", "⚽ هدف جديد ⚽", "🏀 حلم يتحقق 🏀",
    "⚾ ضربة معلم ⚾", "🎾 ضربة حظ 🎾", "🏐 فريق واحد 🏐",
    "🏉 روح الفريق 🏉", "🎱 لعبة الحياة 🎱", "🎯 مستهدف 🎯",
    "🎳 إسقاط الصعاب 🎳", "🎲 حظي حلو 🎲", "🎰 جائزة الحياة 🎰",
    "🎮 تحكم بحياتك 🎮", "🎧 موسيقى وهدوء 🎧", "🎤 صوتي مسموع 🎤",
    "🎸 عزف على أوتار الحياة 🎸", "🎹 سيمفونية الحياة 🎹", "🎺 عزف للحياة 🎺",
    "🎷 نغمات ساحرة 🎷", "🥁 إيقاع الحياة 🥁", "🎻 كونشرتو الحب 🎻",
    "🎵 موسيقى الروح 🎵", "🎶 نغمات الأمل 🎶", "🎼 لحن الحياة 🎼",
]

# ============= 200 بايو إنستجرام =============
INSTAGRAM_BIOS = [
    "📸 | Just vibes ✨", "💫 | Living my best life", "❤️ | Love & Peace",
    "🎯 | Dream chaser", "🌙 | Night owl", "🔥 | Hustle mode",
    "🕊️ | Free soul", "⭐ | Star stuff", "💎 | Rare breed",
    "👑 | Born to shine", "🎨 | Art enthusiast", "📚 | Book lover",
    "✈️ | Travel addict", "🎵 | Music is life", "💪 | Fitness journey",
    "🧘 | Spiritual being", "🤍 | Simplicity", "⚡ | Energy matters",
    "🌊 | Ocean soul", "🌸 | Flower child", "🌹 | Rose gold",
    "🦋 | Butterfly effect", "🐺 | Lone wolf", "🦁 | Lion heart",
    "🐉 | Dragon spirit", "🕊️ | Peace keeper", "🌈 | Colorful mind",
    "☀️ | Sunshine", "🌙 | Moon child", "⭐ | Star gazer",
    "🌍 | Earth lover", "🌿 | Nature soul", "🍃 | Free spirit",
    "🍂 | Autumn soul", "❄️ | Winter child", "🌸 | Spring heart",
    "☕ | Coffee addict", "🍕 | Pizza lover", "🍣 | Sushi master",
    "🍜 | Noodle life", "🍔 | Burger fan", "🍦 | Ice cream dream",
    "🍩 | Donut worry", "🍫 | Chocolate lover", "🍪 | Cookie monster",
    "🍷 | Wine not", "🍺 | Beer lover", "🥂 | Cheers",
    "🎮 | Gamer", "💻 | Tech nerd", "📱 | Digital native",
    "🎬 | Movie buff", "📺 | Series addict", "🎭 | Drama queen",
    "🎪 | Circus life", "🎨 | Creative mind", "📸 | Photography",
    "🎥 | Story teller", "🎞️ | Film maker", "📝 | Writer",
    "🎤 | Singer", "🎸 | Guitarist", "🎹 | Pianist",
    "🥁 | Drummer", "🎻 | Violinist", "🎺 | Trumpet",
    "🎷 | Sax player", "🎵 | Melody maker", "🎶 | Harmony",
    "💃 | Dancer", "🕺 | Dancing king", "🏃 | Runner",
    "🚴 | Cyclist", "🏊 | Swimmer", "🏋️ | Gym rat",
    "🧘 | Yogi", "🥋 | Martial arts", "⚽ | Football",
    "🏀 | Basketball", "🎾 | Tennis", "🏐 | Volleyball",
    "🏈 | Football", "⚾ | Baseball", "🥊 | Boxing",
    "🎯 | Archery", "🏹 | Hunter", "🎣 | Fisherman",
    "🏄 | Surfer", "⛷️ | Skier", "🏂 | Snowboarder",
    "🚣 | Rower", "🧗 | Climber", "🏇 | Rider",
    "🚀 | Space explorer", "🌌 | Galaxy traveler", "🛸 | Alien",
    "🧙 | Wizard", "🧚 | Fairy", "🧛 | Vampire",
    "🧟 | Zombie", "🤖 | Robot", "👽 | Alien",
    "👾 | Gamer", "🎭 | Performer", "🎪 | Entertainer",
]

# ============= 200 بايو ماسنجر =============
MESSENGER_BIOS = [
    "💬 | متاح للكلام أحيانًا", "🎮 | Gaming mode on", "📱 | Offline life online",
    "💭 | أفكار عشوائية", "🎧 | Music is life", "📚 | قراءة وكتابة",
    "🌍 | عابر سبيل", "⚡ | سريع الاستجابة", "😴 | Nap time",
    "💼 | Work mode", "🎯 | Focused", "🤝 | Open for chat",
    "📝 | Busy writing", "🎨 | Creative mode", "🏃 | On the go",
    "🍕 | Food lover", "☕ | Coffee time", "🎬 | Movie time",
    "📺 | Series marathon", "🎮 | Gaming session", "📸 | Photo editing",
    "🎵 | Music session", "📖 | Reading time", "✍️ | Writing mode",
    "🧘 | Meditation", "🏋️ | Workout", "🚶 | Walking",
    "🏃‍♂️ | Running", "🚴 | Cycling", "🏊 | Swimming",
    "🎯 | Goal setting", "📈 | Business mode", "💡 | Ideas",
    "🤔 | Thinking", "😊 | Happy", "😢 | Sad",
    "😍 | In love", "😎 | Cool", "🤓 | Nerd",
    "🥳 | Party", "🎉 | Celebration", "🎊 | Joy",
    "🎈 | Fun", "🎁 | Surprise", "🎀 | Gift",
    "🌸 | Flower", "🌹 | Rose", "🌺 | Hibiscus",
    "🌻 | Sunflower", "🌼 | Daisy", "🌷 | Tulip",
    "🍀 | Lucky", "🎋 | Wishes", "🎍 | Bamboo",
    "🪴 | Plant", "🌵 | Cactus", "🌿 | Herb",
    "🍃 | Leaf", "🍂 | Autumn", "🍁 | Maple",
    "🌾 | Rice", "🌽 | Corn", "🍎 | Apple",
    "🍐 | Pear", "🍊 | Orange", "🍋 | Lemon",
    "🍌 | Banana", "🍉 | Watermelon", "🍇 | Grapes",
    "🍓 | Strawberry", "🫐 | Blueberry", "🍒 | Cherry",
    "🍑 | Peach", "🥭 | Mango", "🥝 | Kiwi",
    "🥑 | Avocado", "🥥 | Coconut", "🥦 | Broccoli",
    "🥬 | Lettuce", "🥒 | Cucumber", "🌶️ | Pepper",
    "🧄 | Garlic", "🧅 | Onion", "🥔 | Potato",
    "🍠 | Sweet potato", "🥕 | Carrot", "🌽 | Corn",
    "🍞 | Bread", "🥖 | Baguette", "🥨 | Pretzel",
    "🧀 | Cheese", "🍳 | Breakfast", "🥚 | Egg",
    "🍗 | Chicken", "🥩 | Steak", "🍔 | Burger",
    "🍟 | Fries", "🌭 | Hot dog", "🍕 | Pizza",
    "🥪 | Sandwich", "🌮 | Taco", "🌯 | Burrito",
    "🥙 | Falafel", "🥗 | Salad", "🍲 | Soup",
    "🍛 | Curry", "🍜 | Noodles", "🍝 | Pasta",
    "🥟 | Dumpling", "🍣 | Sushi", "🍱 | Bento",
    "🥡 | Takeout", "🍦 | Ice cream", "🍨 | Sundae",
    "🍧 | Shaved ice", "🎂 | Cake", "🍰 | Dessert",
    "🍪 | Cookie", "🍩 | Donut", "🍫 | Chocolate",
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
            "📝 **اختر نوع البايو:**\n\n"
            "• 💚 **واتساب** - بايوهات واتساب مميزة\n"
            "• 📸 **إنستجرام** - بايوهات إنستجرام عصرية\n"
            "• 💬 **ماسنجر** - بايوهات ماسنجر متنوعة\n\n"
            f"✨ **يوجد {len(WHATSAPP_BIOS)} بايو لكل قسم**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("bio_"))
    def show_bio(call):
        """عرض بايو واحد عشوائي"""
        bio_type = call.data.split("_")[1]
        
        if bio_type == "whatsapp":
            bio = random.choice(WHATSAPP_BIOS)
            title = "💚 **بايو واتساب:** 💚"
            emoji = "💚"
            total = len(WHATSAPP_BIOS)
        elif bio_type == "instagram":
            bio = random.choice(INSTAGRAM_BIOS)
            title = "📸 **بايو إنستجرام:** 📸"
            emoji = "📸"
            total = len(INSTAGRAM_BIOS)
        else:
            bio = random.choice(MESSENGER_BIOS)
            title = "💬 **بايو ماسنجر:** 💬"
            emoji = "💬"
            total = len(MESSENGER_BIOS)
        
        # حذف الرسالة السابقة
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        # عرض البايو في رسالة منفصلة
        response = f"{title}\n\n`{bio}`\n\n✨ **لنسخ البايو اضغط على النص أعلاه**"
        
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🔄 بايو جديد", callback_data=f"refresh_bio_{bio_type}")
        btn2 = InlineKeyboardButton("📋 نسخ", callback_data=f"copy_bio_{bio_type}_{bio[:50]}")
        btn3 = InlineKeyboardButton("🔙 رجوع", callback_data="bios")
        markup.add(btn1, btn2)
        markup.add(btn3)
        
        bot.send_message(
            call.message.chat.id,
            response,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id, f"✨ {emoji} بايو جديد")
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("refresh_bio_"))
    def refresh_bio(call):
        """تحديث البايو"""
        bio_type = call.data.split("_")[2]
        
        if bio_type == "whatsapp":
            bio = random.choice(WHATSAPP_BIOS)
            title = "💚 **بايو واتساب:** 💚"
            emoji = "💚"
        elif bio_type == "instagram":
            bio = random.choice(INSTAGRAM_BIOS)
            title = "📸 **بايو إنستجرام:** 📸"
            emoji = "📸"
        else:
            bio = random.choice(MESSENGER_BIOS)
            title = "💬 **بايو ماسنجر:** 💬"
            emoji = "💬"
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        response = f"{title}\n\n`{bio}`\n\n✨ **لنسخ البايو اضغط على النص أعلاه**"
        
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🔄 بايو جديد", callback_data=f"refresh_bio_{bio_type}")
        btn2 = InlineKeyboardButton("📋 نسخ", callback_data=f"copy_bio_{bio_type}_{bio[:50]}")
        btn3 = InlineKeyboardButton("🔙 رجوع", callback_data="bios")
        markup.add(btn1, btn2)
        markup.add(btn3)
        
        bot.send_message(
            call.message.chat.id,
            response,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id, f"✨ {emoji} بايو جديد")
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("copy_bio_"))
    def copy_bio(call):
        """تنبيه نسخ البايو"""
        bot.answer_callback_query(call.id, "📋 تم نسخ البايو! يمكنك لصقه الآن", show_alert=False)