import os
import telebot
from handlers.start_handler import register_start_handlers
from handlers.decoration_handler import register_decoration_handlers
from handlers.translation_handler import register_translation_handlers
from handlers.callback_handler import register_callback_handlers

# جلب التوكن
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# تسجيل جميع المعالجات
register_start_handlers(bot)
register_decoration_handlers(bot)
register_translation_handlers(bot)
register_callback_handlers(bot)

if __name__ == "__main__":
    print("=" * 50)
    print("✅ بوت الزخرفة والترجمة المتقدم يعمل...")
    print(f"🤖 @{bot.get_me().username}")
    print("=" * 50)
    print("📊 المميزات:")
    print("   🎨 25+ خط عربي")
    print("   🆎 11+ خط إنجليزي")
    print("   🇰🇷 9+ ترجمة كورية")
    print("   🇨🇳 9+ ترجمة صينية")
    print("   𓂀 10+ ترجمة فرعونية")
    print("=" * 50)
    bot.infinity_polling()