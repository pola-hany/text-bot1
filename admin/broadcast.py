from datetime import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

# تخزين رسائل البث المؤقتة
broadcast_messages = {}

class BroadcastManager:
    
    @staticmethod
    def show_broadcast_panel(bot: TeleBot, chat_id, message_id=None):
        """عرض لوحة البث الجماعي"""
        markup = InlineKeyboardMarkup(row_width=2)
        btn_all = InlineKeyboardButton("📢 لجميع المستخدمين", callback_data="admin_broadcast_all")
        btn_active = InlineKeyboardButton("🔥 للنشطين فقط", callback_data="admin_broadcast_active")
        btn_new = InlineKeyboardButton("✨ للجدد فقط", callback_data="admin_broadcast_new")
        btn_cancel = InlineKeyboardButton("❌ إلغاء", callback_data="admin_broadcast_cancel")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        
        markup.add(btn_all, btn_active)
        markup.add(btn_new)
        markup.add(btn_cancel)
        markup.add(btn_back)
        
        text = """
📢 **الرسائل الجماعية** 📢

📝 **أرسل الرسالة التي تريد نشرها**
• يمكنك إرسال نص عادي
• يمكنك إرسال صورة أو فيديو مع تعليق

🎯 **اختر المستهدفين من الأزرار أدناه بعد إرسال الرسالة**
        """
        
        if message_id:
            try:
                bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
            except:
                bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
            
            msg = bot.send_message(chat_id, "📝 **أرسل الرسالة الآن:**", parse_mode='Markdown')
            bot.register_next_step_handler(msg, BroadcastManager.save_message)
    
    @staticmethod
    def save_message(message):
        """حفظ رسالة البث"""
        from admin.admin_handler import is_admin
        
        chat_id = message.chat.id
        
        # التحقق من أن المرسل أدمن
        if not is_admin(message.from_user.id):
            bot.send_message(chat_id, "⛔ غير مصرح لك", parse_mode='Markdown')
            return
        
        # حفظ الرسالة
        broadcast_messages[str(chat_id)] = {
            'text': message.text if message.text else "",
            'type': 'text',
            'target': None,
            'message_id': message.message_id
        }
        
        # عرض قائمة اختيار المستهدفين
        markup = InlineKeyboardMarkup(row_width=2)
        btn_all = InlineKeyboardButton("📢 لجميع المستخدمين", callback_data=f"broadcast_target_all_{chat_id}")
        btn_active = InlineKeyboardButton("🔥 للنشطين فقط", callback_data=f"broadcast_target_active_{chat_id}")
        btn_new = InlineKeyboardButton("✨ للجدد فقط", callback_data=f"broadcast_target_new_{chat_id}")
        btn_cancel = InlineKeyboardButton("❌ إلغاء", callback_data=f"broadcast_cancel_{chat_id}")
        markup.add(btn_all, btn_active)
        markup.add(btn_new)
        markup.add(btn_cancel)
        
        bot.send_message(
            chat_id,
            f"✅ **تم حفظ الرسالة!**\n\n"
            f"📝 نص الرسالة:\n`{message.text[:200]}{'...' if len(message.text) > 200 else ''}`\n\n"
            f"🎯 **اختر المستهدفين:**",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @staticmethod
    def send_broadcast(bot: TeleBot, chat_id, target):
        """إرسال البث الجماعي"""
        key = str(chat_id)
        msg_data = broadcast_messages.get(key)
        
        if not msg_data:
            bot.send_message(chat_id, "❌ **لم يتم العثور على رسالة**\n📌 يرجى إرسال الرسالة أولاً", parse_mode='Markdown')
            return
        
        # تحديد المستهدفين
        if target == 'all':
            users = db.get_all_users()
            target_name = "جميع المستخدمين"
        elif target == 'active':
            users = db.get_active_users()
            target_name = "النشطين"
        elif target == 'new':
            users = db.get_new_users()
            target_name = "الجدد"
        else:
            bot.send_message(chat_id, "❌ **هدف غير صالح**", parse_mode='Markdown')
            return
        
        total = len(users)
        
        if total == 0:
            bot.send_message(chat_id, f"❌ **لا يوجد {target_name} للإرسال إليهم**", parse_mode='Markdown')
            return
        
        success = 0
        failed = 0
        
        # رسالة بدء الإرسال
        status_msg = bot.send_message(
            chat_id,
            f"🚀 **بدء الإرسال إلى {target_name}...**\n📊 العدد الإجمالي: {total}",
            parse_mode='Markdown'
        )
        
        text_to_send = msg_data['text']
        
        for user in users:
            try:
                user_id = user.get('user_id') if isinstance(user, dict) else user
                if isinstance(user_id, str) and user_id.isdigit():
                    user_id = int(user_id)
                
                # إرسال الرسالة
                bot.send_message(user_id, text_to_send, parse_mode='Markdown')
                success += 1
                
            except Exception as e:
                failed += 1
                print(f"⚠️ فشل الإرسال إلى {user_id}: {e}")
            
            # تحديث كل 5 رسائل
            if (success + failed) % 5 == 0:
                try:
                    bot.edit_message_text(
                        f"🚀 **جاري الإرسال...**\n✅ تم: {success}\n❌ فشل: {failed}\n📊 المتبقي: {total - (success + failed)}",
                        chat_id,
                        status_msg.message_id,
                        parse_mode='Markdown'
                    )
                except:
                    pass
        
        # تقرير الإرسال
        report = f"""
✅ **تم الانتهاء من الإرسال!**

📊 **التقرير:**
• ✅ تم الإرسال بنجاح: `{success}`
• ❌ فشل الإرسال: `{failed}`
• 🎯 المستهدفين: `{target_name}`
• 📅 التاريخ: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

📝 **نص الرسالة:**
`{text_to_send[:200]}{'...' if len(text_to_send) > 200 else ''}`
        """
        
        markup = InlineKeyboardMarkup()
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_back)
        
        try:
            bot.edit_message_text(report, chat_id, status_msg.message_id, parse_mode='Markdown', reply_markup=markup)
        except:
            bot.send_message(chat_id, report, parse_mode='Markdown', reply_markup=markup)
        
        # حفظ في السجلات
        db.add_log(f"Broadcast sent to {success} users ({target_name})", "admin")
        
        # مسح الرسالة المخزنة
        if key in broadcast_messages:
            del broadcast_messages[key]
    
    @staticmethod
    def cancel_broadcast(bot: TeleBot, chat_id):
        """إلغاء البث"""
        key = str(chat_id)
        if key in broadcast_messages:
            del broadcast_messages[key]
            bot.send_message(chat_id, "❌ **تم إلغاء البث الجماعي**", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "⚠️ **لا يوجد بث نشط**", parse_mode='Markdown')
        
        # العودة للوحة التحكم
        from .admin_panel import AdminPanel
        AdminPanel.show_main_panel(bot, chat_id)