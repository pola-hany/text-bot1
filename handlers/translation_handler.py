import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fonts.korean_fonts import KOREAN_STYLES
from fonts.chinese_fonts import CHINESE_STYLES
from fonts.egyptian_fonts import EGYPTIAN_STYLES
from database.db_manager import Database

db = Database()
user_texts = {}

def register_translation_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "translate")
    def translate_callback(call):
        """طلب الترجمة - عرض اختيار اللغة أولاً"""
        bot.answer_callback_query(call.id, "🌍 اختر لغة الترجمة")
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("🇰🇷 كوري", callback_data="trans_lang_korean")
        btn2 = InlineKeyboardButton("🇨🇳 صيني", callback_data="trans_lang_chinese")
        btn3 = InlineKeyboardButton("𓂀 فرعوني", callback_data="trans_lang_egyptian")
        btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
        markup.add(btn1, btn2, btn3)
        markup.add(btn4)
        
        bot.edit_message_text(
            "🌍 **ترجمة الأسماء** 🌍\n\n"
            "📌 **اختر لغة الترجمة:**\n\n"
            "• 🇰🇷 **كوري** - ترجمة إلى اللغة الكورية\n"
            "• 🇨🇳 **صيني** - ترجمة إلى اللغة الصينية\n"
            "• 𓂀 **فرعوني** - ترجمة إلى الهيروغليفية المصرية القديمة\n\n"
            "✅ سيتم الترجمة بعد إرسال النص",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("trans_lang_"))
    def handle_lang_selection(call):
        """معالج اختيار اللغة - طلب إدخال النص"""
        lang = call.data.split("_")[2]
        
        lang_names = {
            "korean": "الكورية",
            "chinese": "الصينية",
            "egyptian": "الفرعونية"
        }
        
        lang_emojis = {
            "korean": "🇰🇷",
            "chinese": "🇨🇳",
            "egyptian": "𓂀"
        }
        
        bot.answer_callback_query(call.id, f"📝 أرسل النص للترجمة إلى {lang_names.get(lang, lang)}")
        
        # حفظ اللغة المختارة للمستخدم
        user_texts[call.message.chat.id] = {"lang": lang, "text": None}
        
        msg = bot.send_message(
            call.message.chat.id,
            f"📝 **أرسل الاسم أو النص للترجمة:**\n\n"
            f"✨ **اللغة المختارة:** {lang_emojis.get(lang, '')} {lang_names.get(lang, lang)}\n\n"
            f"✅ يمكنك إرسال نص **عربي** أو **إنجليزي**\n\n"
            f"❌ لإلغاء العملية أرسل `cancel`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_translation, lang, bot)
    
    def process_translation(message, lang, bot):
        """معالجة النص وعرض الترجمة"""
        chat_id = message.chat.id
        text = message.text.strip()
        
        # التحقق من إلغاء العملية
        if text.lower() == 'cancel':
            bot.send_message(
                chat_id,
                "❌ **تم إلغاء العملية**\n\nيمكنك العودة للقائمة الرئيسية بـ /start",
                parse_mode='Markdown'
            )
            return
        
        # حذف رسالة المستخدم لتجنب الازدحام
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        
        # عرض الترجمة حسب اللغة المختارة
        if lang == "korean":
            send_korean_translations(bot, chat_id, text)
        elif lang == "chinese":
            send_chinese_translations(bot, chat_id, text)
        else:
            send_egyptian_translations(bot, chat_id, text)
        
        # تحديث نشاط المستخدم في قاعدة البيانات
        db.update_user_activity(message.from_user.id, "translation")
        bot.answer_callback_query(message.message_id, "✨ تمت الترجمة")

def send_korean_translations(bot, chat_id, text):
    """إرسال الترجمات الكورية"""
    selected = random.sample(KOREAN_STYLES, min(8, len(KOREAN_STYLES)))
    
    for style in selected:
        try:
            translated = style["func"](text)
            msg = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except Exception as e:
            print(f"⚠️ خطأ في الترجمة الكورية: {e}")
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🔄 ترجمة جديدة", callback_data="translate")
    btn2 = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    
    bot.send_message(
        chat_id,
        "🇰🇷 **للحصول على ترجمات كورية أخرى:**",
        parse_mode='Markdown',
        reply_markup=markup
    )

def send_chinese_translations(bot, chat_id, text):
    """إرسال الترجمات الصينية"""
    selected = random.sample(CHINESE_STYLES, min(8, len(CHINESE_STYLES)))
    
    for style in selected:
        try:
            translated = style["func"](text)
            msg = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except Exception as e:
            print(f"⚠️ خطأ في الترجمة الصينية: {e}")
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🔄 ترجمة جديدة", callback_data="translate")
    btn2 = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    
    bot.send_message(
        chat_id,
        "🇨🇳 **للحصول على ترجمات صينية أخرى:**",
        parse_mode='Markdown',
        reply_markup=markup
    )

def send_egyptian_translations(bot, chat_id, text):
    """إرسال الترجمات الفرعونية"""
    selected = random.sample(EGYPTIAN_STYLES, min(8, len(EGYPTIAN_STYLES)))
    
    for style in selected:
        try:
            translated = style["func"](text)
            msg = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except Exception as e:
            print(f"⚠️ خطأ في الترجمة الفرعونية: {e}")
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🔄 ترجمة جديدة", callback_data="translate")
    btn2 = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    
    bot.send_message(
        chat_id,
        "𓂀 **للحصول على ترجمات فرعونية أخرى:**",
        parse_mode='Markdown',
        reply_markup=markup
    )