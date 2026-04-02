import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class Database:
    # أضف هذه الدوال في class Database:

    def get_required_channels(self):
        """الحصول على قائمة القنوات الإجبارية"""
        return self.data.get('required_channels', [])
    
    def add_required_channel(self, channel):
        """إضافة قناة إجبارية"""
        if 'required_channels' not in self.data:
            self.data['required_channels'] = []
        
        # التأكد من عدم وجود القناة مسبقاً
        for existing in self.data['required_channels']:
            if existing['chat_id'] == channel['chat_id']:
                return False
        
        self.data['required_channels'].append(channel)
        self._save_data()
        return True
    
    def remove_required_channel(self, chat_id):
        """حذف قناة إجبارية"""
        if 'required_channels' in self.data:
            self.data['required_channels'] = [
                ch for ch in self.data['required_channels'] 
                if ch['chat_id'] != chat_id
            ]
            self._save_data()
            return True
        return False
    """مدير قاعدة البيانات - نسخة مبسطة باستخدام JSON"""
    
    def __init__(self, db_file='database.json'):
        self.db_file = db_file
        self.data = self._load_data()
    
    def _load_data(self):
        """تحميل البيانات من الملف"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._init_data()
        return self._init_data()
    
    def _init_data(self):
        """تهيئة البيانات الأساسية"""
        return {
            'users': {},
            'stats': {
                'decoration': 0,
                'translation': 0,
                'bios': 0,
                'effects': 0,
                'daily_requests': {},
                'hourly_requests': {}
            },
            'logs': [],
            'settings': {
                'welcome_message': 'مرحباً بك في البوت!',
                'rate_limit': 30,
                'language': 'arabic',
                'admins': []
            }
        }
    
    def _save_data(self):
        """حفظ البيانات في الملف"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_user(self, user_id, username=None):
        """إضافة مستخدم جديد"""
        user_id = str(user_id)
        if user_id not in self.data['users']:
            self.data['users'][user_id] = {
                'user_id': user_id,
                'username': username,
                'joined_date': datetime.now().isoformat(),
                'last_active': datetime.now().isoformat(),
                'requests': 0,
                'active': True,
                'decoration_count': 0,
                'translation_count': 0,
                'bios_count': 0,
                'effects_count': 0
            }
            self._save_data()
            return True
        return False
    
    def update_user_activity(self, user_id, service=None):
        """تحديث نشاط المستخدم"""
        user_id = str(user_id)
        if user_id in self.data['users']:
            self.data['users'][user_id]['last_active'] = datetime.now().isoformat()
            self.data['users'][user_id]['requests'] += 1
            
            if service == 'decoration':
                self.data['users'][user_id]['decoration_count'] += 1
                self.data['stats']['decoration'] += 1
            elif service == 'translation':
                self.data['users'][user_id]['translation_count'] += 1
                self.data['stats']['translation'] += 1
            elif service == 'bios':
                self.data['users'][user_id]['bios_count'] += 1
                self.data['stats']['bios'] += 1
            elif service == 'effects':
                self.data['users'][user_id]['effects_count'] += 1
                self.data['stats']['effects'] += 1
            
            # تحديث الإحصائيات اليومية
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in self.data['stats']['daily_requests']:
                self.data['stats']['daily_requests'][today] = 0
            self.data['stats']['daily_requests'][today] += 1
            
            # تحديث الإحصائيات الساعية
            hour = datetime.now().strftime('%H')
            if hour not in self.data['stats']['hourly_requests']:
                self.data['stats']['hourly_requests'][hour] = 0
            self.data['stats']['hourly_requests'][hour] += 1
            
            self._save_data()
    
    def get_user(self, user_id):
        """الحصول على معلومات المستخدم"""
        return self.data['users'].get(str(user_id))
    
    def get_user_count(self):
        """عدد المستخدمين الكلي"""
        return len(self.data['users'])
    
    def get_active_users_today(self):
        """عدد المستخدمين النشطين اليوم"""
        today = datetime.now().strftime('%Y-%m-%d')
        count = 0
        for user in self.data['users'].values():
            if user.get('last_active', '').startswith(today):
                count += 1
        return count
    
    def get_active_users_week(self):
        """عدد المستخدمين النشطين خلال الأسبوع"""
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        count = 0
        for user in self.data['users'].values():
            if user.get('last_active', '') > week_ago:
                count += 1
        return count
    
    def get_new_users_today(self):
        """عدد المستخدمين الجدد اليوم"""
        today = datetime.now().strftime('%Y-%m-%d')
        count = 0
        for user in self.data['users'].values():
            if user.get('joined_date', '').startswith(today):
                count += 1
        return count
    
    def get_new_users_week(self):
        """عدد المستخدمين الجدد خلال الأسبوع"""
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        count = 0
        for user in self.data['users'].values():
            if user.get('joined_date', '') > week_ago:
                count += 1
        return count
    
    def get_new_users_month(self):
        """عدد المستخدمين الجدد خلال الشهر"""
        month_ago = (datetime.now() - timedelta(days=30)).isoformat()
        count = 0
        for user in self.data['users'].values():
            if user.get('joined_date', '') > month_ago:
                count += 1
        return count
    
    def get_service_stats(self):
        """إحصائيات الخدمات"""
        return {
            'decoration': self.data['stats']['decoration'],
            'translation': self.data['stats']['translation'],
            'bios': self.data['stats']['bios'],
            'effects': self.data['stats']['effects']
        }
    
    def get_peak_hours(self):
        """أوقات الذروة"""
        hours = self.data['stats']['hourly_requests']
        sorted_hours = sorted(hours.items(), key=lambda x: x[1], reverse=True)[:3]
        text = ""
        for hour, count in sorted_hours:
            text += f"• الساعة {hour}:00 → {count} طلب\n"
        return text or "لا توجد بيانات كافية"
    
    def get_daily_avg(self):
        """متوسط الطلبات اليومية"""
        daily = self.data['stats']['daily_requests']
        if not daily:
            return 0
        return sum(daily.values()) // len(daily)
    
    def get_db_size(self):
        """حجم قاعدة البيانات"""
        if os.path.exists(self.db_file):
            size = os.path.getsize(self.db_file)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        return "0 B"
    
    def get_all_users(self, limit=None, offset=0):
        """الحصول على جميع المستخدمين"""
        users = list(self.data['users'].values())
        if limit:
            return users[offset:offset + limit]
        return users
    
    def get_active_users(self):
        """الحصول على المستخدمين النشطين"""
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        return [u for u in self.data['users'].values() if u.get('last_active', '') > week_ago]
    
    def get_new_users(self):
        """الحصول على المستخدمين الجدد"""
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        return [u for u in self.data['users'].values() if u.get('joined_date', '') > week_ago]
    
    def get_all_data(self):
        """الحصول على جميع البيانات للنسخ الاحتياطي"""
        return self.data
    
    def add_log(self, action, user="system"):
        """إضافة سجل"""
        self.data['logs'].append({
            'time': datetime.now().isoformat(),
            'action': action,
            'user': user
        })
        # الاحتفاظ بآخر 1000 سجل فقط
        if len(self.data['logs']) > 1000:
            self.data['logs'] = self.data['logs'][-1000:]
        self._save_data()
    
    def get_logs(self, limit=10, offset=0):
        """الحصول على السجلات"""
        return self.data['logs'][::-1][offset:offset + limit]
    
    def get_logs_count(self):
        """عدد السجلات"""
        return len(self.data['logs'])
    
    def get_settings(self):
        """الحصول على الإعدادات"""
        return self.data['settings']
    
    def update_setting(self, key, value):
        """تحديث إعداد"""
        self.data['settings'][key] = value
        self._save_data()