from telebot import TeleBot
from keyboards.menus import main_menu

def register_callback_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
    def back_to_menu(call):
        bot.edit_message_text(
            "✨ **القائمة الرئيسية** ✨\n\nاختر الخدمة:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=main_menu(call.from_user.id)
        )
        bot.answer_callback_query(call.id)