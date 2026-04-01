from telebot import TeleBot
from keyboards.menus import main_menu

def register_callback_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "menu")
    def back_to_menu(call):
        """العودة للقائمة الرئيسية"""
        bot.edit_message_text(
            "✨ **القائمة الرئيسية** ✨\n\n"
            "📌 **اختر الخدمة التي تريدها:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id)
    
    @bot.callback_query_handler(func=lambda call: call.data == "new_name")
    def new_name(call):
        """طلب اسم جديد"""
        bot.edit_message_text(
            "📝 **أرسل النص الجديد:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)