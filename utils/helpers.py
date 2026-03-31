# دوال مساعدة للاستخدام المستقبلي
def format_text(text, font_func):
    """تنسيق النص باستخدام دالة الخط"""
    try:
        return font_func(text)
    except:
        return text