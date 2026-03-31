from telebot import TeleBot
from keyboards.menus import main_menu
from handlers.decoration_handler import send_decorations

def register_callback_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        user_id = call.message.chat.id
        name = bot.get_user_name(user_id) if hasattr(bot, 'get_user_name') else ""
        
        if call.data == "menu":
            bot.edit_message_text(
                "✨ **القائمة الرئيسية** ✨\n\nأرسل اسمك للبدء:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            bot.register_next_step_handler(call.message, lambda m: None)
            bot.answer_callback_query(call.id)
            return
        
        if call.data == "new_name":
            bot.edit_message_text(
                "📝 **أرسل الاسم الجديد:**",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id)
            return
        
        if not name:
            bot.answer_callback_query(call.id, "⚠️ يرجى إرسال الاسم أولاً", show_alert=True)
            return
        
        if call.data == "arabic":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send_decorations(bot, call.message.chat.id, name, "arabic")
            bot.answer_callback_query(call.id, "✨ جاري توليد الزخارف...")
        
        elif call.data == "english":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send_decorations(bot, call.message.chat.id, name, "english")
            bot.answer_callback_query(call.id, "✨ جاري توليد الزخارف...")
        
        elif call.data.startswith("more_"):
            parts = call.data.split("_", 2)
            lang = parts[1]
            name_text = parts[2]
            
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send_decorations(bot, call.message.chat.id, name_text, lang)
            bot.answer_callback_query(call.id, "✨ جاري توليد المزيد...")