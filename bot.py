import os
import telebot
from handlers import register_all_handlers

# جلب التوكن
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# تسجيل جميع المعالجات
register_all_handlers(bot)

if __name__ == "__main__":
    print("=" * 50)
    print("✅ بوت الزخرفة والترجمة المتقدم يعمل...")
    print(f"🤖 @{bot.get_me().username}")
    print("=" * 50)
    print("📊 المميزات:")
    print("   🎨 25+ خط عربي")
    print("   🆎 11+ خط إنجليزي")
    print("   🇰🇷 8+ ترجمة كورية")
    print("   🇨🇳 8+ ترجمة صينية")
    print("   𓂀 8+ ترجمة فرعونية")
    print("   📝 بايوهات جاهزة")
    print("   🎨 تأثيرات إضافية")
    print("=" * 50)
    bot.infinity_polling()