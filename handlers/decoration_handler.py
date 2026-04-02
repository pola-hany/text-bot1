import random
import re
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fonts.arabic_fonts import ARABIC_FONTS
from fonts.english_fonts import ENGLISH_FONTS
from database.db_manager import Database

db = Database()
user_data = {}

def is_arabic(text):
    """التحقق من أن النص عربي"""
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+')
    return bool(arabic_pattern.search(text))

def is_english(text):
    """التحقق من أن النص إنجليزي"""
    english_pattern = re.compile(r'^[a-zA-Z\s]+$')
    return bool(english_pattern.match(text.strip()))

def register_decoration_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "decorate")
    def decorate_callback(call):
        """طلب زخرفة النصوص - عرض اختيار اللغة أولاً"""
        bot.answer_callback_query(call.id, "🎨 اختر لغة الزخرفة")
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("🇸🇦 عربي", callback_data="deco_lang_arabic")
        btn2 = InlineKeyboardButton("🇬🇧 إنجليزي", callback_data="deco_lang_english")
        btn3 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
        markup.add(btn1, btn2)
        markup.add(btn3)
        
        bot.edit_message_text(
            "🎨 **زخرفة النصوص** 🎨\n\n"
            "📌 **اختر لغة الزخرفة أولاً:**\n\n"
            "• **عربي** - للزخرفة العربية\n"
            "• **إنجليزي** - للزخرفة الإنجليزية\n\n"
            "⚠️ **ملاحظة:** سيتم التحقق من صحة اللغة بعد إدخال النص",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("deco_lang_"))
    def handle_lang_selection(call):
        """معالج اختيار اللغة - طلب إدخال النص"""
        lang = call.data.split("_")[2]
        
        # حفظ اللغة المختارة للمستخدم
        user_data[call.message.chat.id] = {"lang": lang, "text": None}
        
        lang_name = "العربية" if lang == "arabic" else "الإنجليزية"
        
        bot.answer_callback_query(call.id, f"📝 أرسل الاسم {lang_name}")
        
        msg = bot.send_message(
            call.message.chat.id,
            f"📝 **أرسل الاسم {'باللغة العربية' if lang == 'arabic' else 'باللغة الإنجليزية'}:**\n\n"
            f"✨ **اللغة المختارة:** {'🇸🇦 عربي' if lang == 'arabic' else '🇬🇧 إنجليزي'}\n\n"
            f"⚠️ **تنبيه:** يجب أن يكون النص {'باللغة العربية فقط' if lang == 'arabic' else 'باللغة الإنجليزية فقط'}\n\n"
            f"✅ سيتم عرض الزخارف بعد إرسال النص\n\n"
            f"❌ لإلغاء العملية أرسل `cancel`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, validate_and_decorate, lang, bot)
    
    def validate_and_decorate(message, lang, bot):
        """التحقق من صحة النص حسب اللغة ثم الزخرفة"""
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
        
        # التحقق من اللغة
        if lang == "arabic":
            if not is_arabic(text):
                markup = InlineKeyboardMarkup()
                btn1 = InlineKeyboardButton("🔄 محاولة مرة أخرى", callback_data="decorate")
                btn2 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
                markup.add(btn1, btn2)
                
                bot.send_message(
                    chat_id,
                    f"❌ **خطأ في اللغة!**\n\n"
                    f"لقد اخترت الزخرفة **العربية** ولكن النص الذي أرسلته:\n"
                    f"`{text[:100]}`\n\n"
                    f"⚠️ هذا النص **ليس باللغة العربية**\n\n"
                    f"📌 **يرجى إرسال اسم عربي صحيح**\n\n"
                    f"مثال: محمد، أحمد، فاطمة، نور",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
                return
        else:  # english
            if not is_english(text):
                markup = InlineKeyboardMarkup()
                btn1 = InlineKeyboardButton("🔄 محاولة مرة أخرى", callback_data="decorate")
                btn2 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
                markup.add(btn1, btn2)
                
                bot.send_message(
                    chat_id,
                    f"❌ **خطأ في اللغة!**\n\n"
                    f"لقد اخترت الزخرفة **الإنجليزية** ولكن النص الذي أرسلته:\n"
                    f"`{text[:100]}`\n\n"
                    f"⚠️ هذا النص **ليس باللغة الإنجليزية**\n\n"
                    f"📌 **يرجى إرسال اسم إنجليزي صحيح**\n\n"
                    f"مثال: Ahmed, Mohamed, Sara, John",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
                return
        
        # النص صحيح - حفظ وعرض الزخارف
        user_data[chat_id] = {"lang": lang, "text": text}
        
        # عرض الزخارف
        if lang == "arabic":
            send_arabic_decorations(bot, chat_id, text)
        else:
            send_english_decorations(bot, chat_id, text)
        
        # تحديث نشاط المستخدم
        db.update_user_activity(message.from_user.id, "decoration")
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("more_deco_"))
    def handle_more_decorations(call):
        """المزيد من الزخارف"""
        parts = call.data.split("_")
        lang = parts[2]
        user_id = call.message.chat.id
        data = user_data.get(user_id, {})
        text = data.get("text", "")
        
        if not text:
            bot.answer_callback_query(call.id, "⚠️ يرجى إعادة إرسال النص", show_alert=True)
            bot.send_message(
                call.message.chat.id,
                "🔄 يرجى اختيار الخدمة من القائمة الرئيسية",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_menu")
                )
            )
            return
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        if lang == "arabic":
            send_arabic_decorations(bot, call.message.chat.id, text)
        else:
            send_english_decorations(bot, call.message.chat.id, text)
        
        bot.answer_callback_query(call.id, "✨ جاري توليد المزيد...")

def send_arabic_decorations(bot, chat_id, text):
    """إرسال الزخارف العربية"""
    selected = random.sample(ARABIC_FONTS, min(10, len(ARABIC_FONTS)))
    
    for font in selected:
        try:
            decorated = font["func"](text)
            msg = f"{font['emoji']} **{font['name']}**\n`{decorated}`\n_{font['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_deco_arabic")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="decorate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        chat_id,
        "🎯 **للحصول على المزيد من الزخارف العربية:**",
        parse_mode='Markdown',
        reply_markup=markup
    )

def send_english_decorations(bot, chat_id, text):
    """إرسال الزخارف الإنجليزية"""
    selected = random.sample(ENGLISH_FONTS, min(10, len(ENGLISH_FONTS)))
    
    for font in selected:
        try:
            decorated = font["func"](text)
            msg = f"{font['emoji']} **{font['name']}**\n`{decorated}`\n_{font['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_deco_english")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="decorate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        chat_id,
        "🎯 **للحصول على المزيد من الزخارف الإنجليزية:**",
        parse_mode='Markdown',
        reply_markup=markup
    )