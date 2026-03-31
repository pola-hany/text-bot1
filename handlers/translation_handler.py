import random
from telebot import TeleBot
from keyboards.menus import translation_menu, get_translation_more_button
from fonts.korean_fonts import KOREAN_STYLES
from fonts.chinese_fonts import CHINESE_STYLES
from fonts.egyptian_fonts import EGYPTIAN_STYLES

# تخزين أسماء المستخدمين للترجمة
user_names = {}

def save_translation_name(bot: TeleBot, message):
    """حفظ اسم المستخدم للترجمة"""
    user_names[message.chat.id] = message.text
    bot.send_message(
        message.chat.id,
        f"✅ تم استلام: **{message.text}**\n\n"
        f"🌍 **اختر لغة الترجمة:**",
        parse_mode='Markdown',
        reply_markup=translation_menu()
    )

def send_translations(bot: TeleBot, chat_id, name, lang):
    """إرسال الترجمات كل واحدة في رسالة منفصلة"""
    if lang == "korean":
        styles = KOREAN_STYLES
        title_emoji = "🇰🇷"
        title_name = "كورية"
    elif lang == "chinese":
        styles = CHINESE_STYLES
        title_emoji = "🇨🇳"
        title_name = "صينية"
    else:
        styles = EGYPTIAN_STYLES
        title_emoji = "𓂀"
        title_name = "مصرية قديمة"
    
    selected = random.sample(styles, min(8, len(styles)))
    
    for style in selected:
        try:
            translated_text = style["func"](name)
            text = f"{style['emoji']} **{style['name']}**\n`{translated_text}`\n_{style['desc']}_"
            
            bot.send_message(
                chat_id,
                text,
                parse_mode='Markdown',
                reply_markup=None
            )
        except Exception as e:
            continue
    
    # إرسال أزرار التحكم
    bot.send_message(
        chat_id,
        f"🎯 **للحصول على المزيد من الترجمات {title_name}:**",
        parse_mode='Markdown',
        reply_markup=get_translation_more_button(name, lang)
    )

def register_translation_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "translate")
    def translate_callback(call):
        """بدء الترجمة"""
        bot.answer_callback_query(call.id, "🌍 أرسل النص للترجمة")
        msg = bot.send_message(
            call.message.chat.id,
            "🌍 **أرسل الاسم أو النص للترجمة:**\n\n"
            "📌 يمكنك إرسال الاسم بـ:\n"
            "• اللغة العربية\n"
            "• اللغة الإنجليزية\n\n"
            "✨ سيتم الترجمة إلى الكوري، الصيني، والفرعوني",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, lambda m: save_translation_name(bot, m))
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("trans_"))
    def handle_translation_callback(call):
        """معالج اختيار لغة الترجمة"""
        lang = call.data.split("_")[1]
        user_id = call.message.chat.id
        name = user_names.get(user_id, "")
        
        if not name:
            bot.answer_callback_query(call.id, "⚠️ يرجى إرسال النص أولاً", show_alert=True)
            return
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_translations(bot, call.message.chat.id, name, lang)
        bot.answer_callback_query(call.id, f"✨ جاري الترجمة إلى {lang}...")
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("more_trans_"))
    def handle_more_translation(call):
        """المزيد من الترجمات"""
        parts = call.data.split("_", 2)
        lang = parts[2]
        name = user_names.get(call.message.chat.id, "")
        
        if not name:
            bot.answer_callback_query(call.id, "⚠️ يرجى إعادة إرسال النص", show_alert=True)
            return
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_translations(bot, call.message.chat.id, name, lang)
        bot.answer_callback_query(call.id, "✨ جاري توليد المزيد...")