class KoreanFonts:
    """خطوط كورية متنوعة"""
    
    @staticmethod
    def korean_standard(text):
        """كوري قياسي - هانغول"""
        # تحويل النص العربي/الإنجليزي إلى كوري
        korean_map = {
            # حروف عربية
            'ا': '아', 'ب': '바', 'ت': '타', 'ث': '사', 'ج': '자', 'ح': '하',
            'خ': '카', 'د': '다', 'ذ': '자', 'ر': '라', 'ز': '자', 'س': '사',
            'ش': '샤', 'ص': '사', 'ض': '다', 'ط': '타', 'ظ': '자', 'ع': '아',
            'غ': '가', 'ف': '파', 'ق': '카', 'ك': '카', 'ل': '라', 'م': '마',
            'ن': '나', 'ه': '하', 'و': '와', 'ي': '야', 'ء': '으', 'ؤ': '우',
            'ئ': '이', 'آ': '아',
            # حروف إنجليزية
            'a': '아', 'b': '비', 'c': '시', 'd': '디', 'e': '이', 'f': '에프',
            'g': '지', 'h': '에이치', 'i': '아이', 'j': '제이', 'k': '케이', 'l': '엘',
            'm': '엠', 'n': '엔', 'o': '오', 'p': '피', 'q': '큐', 'r': '아르',
            's': '에스', 't': '티', 'u': '유', 'v': '브이', 'w': '더블유', 'x': '엑스',
            'y': '와이', 'z': '제트'
        }
        result = ""
        for char in text:
            if char in korean_map:
                result += korean_map[char]
            elif char.lower() in korean_map:
                result += korean_map[char.lower()]
            else:
                result += char
        return result
    
    @staticmethod
    def korean_cute(text):
        """كوري لطيف - بأحرف كورية منمقة"""
        base = KoreanFonts.korean_standard(text)
        # إضافة رموز لطيفة حول النص
        return f"🌸 {base} 🌸"
    
    @staticmethod
    def korean_cool(text):
        """كوري كول - بأحرف كورية جريئة"""
        base = KoreanFonts.korean_standard(text)
        return f"🔥 {base} 🔥"
    
    @staticmethod
    def korean_elegant(text):
        """كوري أنيق - بأحرف كورية فاخرة"""
        base = KoreanFonts.korean_standard(text)
        return f"✨ {base} ✨"
    
    @staticmethod
    def korean_bold(text):
        """كوري عريض - خط كوري ثقيل"""
        base = KoreanFonts.korean_standard(text)
        return f"💪 {base} 💪"
    
    @staticmethod
    def korean_double(text):
        """كوري مزدوج - حروف كورية مكررة"""
        base = KoreanFonts.korean_standard(text)
        return f"「{base}」"
    
    @staticmethod
    def korean_with_heart(text):
        """كوري بقلوب - مزخرف بقلوب"""
        base = KoreanFonts.korean_standard(text)
        return f"♡ {base} ♡"
    
    @staticmethod
    def korean_with_star(text):
        """كوري بنجوم - مزخرف بنجوم"""
        base = KoreanFonts.korean_standard(text)
        return f"★ {base} ★"
    
    @staticmethod
    def korean_small(text):
        """كوري صغير - أحرف كورية مصغرة"""
        base = KoreanFonts.korean_standard(text)
        return f"ˢᵐᵃˡˡ {base}"

# قائمة الخطوط الكورية
KOREAN_STYLES = [
    {"name": "كوري قياسي", "func": KoreanFonts.korean_standard, "emoji": "🇰🇷", "desc": "ترجمة كورية قياسية"},
    {"name": "كوري لطيف", "func": KoreanFonts.korean_cute, "emoji": "🌸", "desc": "كوري بأسلوب لطيف"},
    {"name": "كوري كول", "func": KoreanFonts.korean_cool, "emoji": "🔥", "desc": "كوري بأسلوب جريء"},
    {"name": "كوري أنيق", "func": KoreanFonts.korean_elegant, "emoji": "✨", "desc": "كوري بأسلوب فاخر"},
    {"name": "كوري عريض", "func": KoreanFonts.korean_bold, "emoji": "💪", "desc": "خط كوري ثقيل"},
    {"name": "كوري مزدوج", "func": KoreanFonts.korean_double, "emoji": "📦", "desc": "كوري بأقواس مزدوجة"},
    {"name": "كوري بقلوب", "func": KoreanFonts.korean_with_heart, "emoji": "❤️", "desc": "كوري مزخرف بقلوب"},
    {"name": "كوري بنجوم", "func": KoreanFonts.korean_with_star, "emoji": "⭐", "desc": "كوري مزخرف بنجوم"},
    {"name": "كوري صغير", "func": KoreanFonts.korean_small, "emoji": "🔤", "desc": "أحرف كورية مصغرة"},
]