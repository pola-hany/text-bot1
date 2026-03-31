class ChineseFonts:
    """خطوط صينية متنوعة"""
    
    @staticmethod
    def chinese_standard(text):
        """صيني قياسي - مبسط"""
        chinese_map = {
            # حروف عربية
            'ا': '阿', 'ب': '巴', 'ت': '塔', 'ث': '萨', 'ج': '贾', 'ح': '哈',
            'خ': '赫', 'د': '达', 'ذ': '扎', 'ر': '拉', 'ز': '扎', 'س': '萨',
            'ش': '沙', 'ص': '萨', 'ض': '达', 'ط': '塔', 'ظ': '扎', 'ع': '阿',
            'غ': '加', 'ف': '法', 'ق': '卡', 'ك': '卡', 'ل': '拉', 'م': '马',
            'ن': '纳', 'ه': '哈', 'و': '瓦', 'ي': '亚', 'ء': '厄', 'ؤ': '乌',
            'ئ': '伊', 'آ': '阿',
            # حروف إنجليزية
            'a': '艾', 'b': '贝', 'c': '西', 'd': '迪', 'e': '伊', 'f': '艾弗',
            'g': '吉', 'h': '艾奇', 'i': '艾', 'j': '杰', 'k': '凯', 'l': '艾尔',
            'm': '艾姆', 'n': '恩', 'o': '奥', 'p': '皮', 'q': '丘', 'r': '阿尔',
            's': '艾斯', 't': '提', 'u': '乌', 'v': '维', 'w': '达布流', 'x': '艾克斯',
            'y': '怀', 'z': '泽德'
        }
        result = ""
        for char in text:
            if char in chinese_map:
                result += chinese_map[char]
            elif char.lower() in chinese_map:
                result += chinese_map[char.lower()]
            else:
                result += char
        return result
    
    @staticmethod
    def chinese_traditional(text):
        """صيني تقليدي -繁体"""
        base = ChineseFonts.chinese_standard(text)
        # تحويل إلى التقليدي (مبسط للعرض)
        traditional_map = {
            '阿': '阿', '巴': '巴', '塔': '塔', '萨': '薩', '贾': '賈', '哈': '哈',
            '赫': '赫', '达': '達', '扎': '紮', '拉': '拉', '沙': '沙', '法': '法',
            '卡': '卡', '马': '馬', '纳': '納', '亚': '亞', '乌': '烏', '伊': '伊',
            '艾': '艾', '贝': '貝', '西': '西', '迪': '迪', '杰': '傑', '凯': '凱',
            '奥': '奧', '皮': '皮', '丘': '丘', '维': '維', '怀': '懷', '泽': '澤'
        }
        result = ""
        for char in base:
            if char in traditional_map:
                result += traditional_map[char]
            else:
                result += char
        return result
    
    @staticmethod
    def chinese_cute(text):
        """صيني لطيف - بأحرف صينية منمقة"""
        base = ChineseFonts.chinese_standard(text)
        return f"🌸 {base} 🌸"
    
    @staticmethod
    def chinese_cool(text):
        """صيني كول - بأحرف صينية جريئة"""
        base = ChineseFonts.chinese_standard(text)
        return f"🔥 {base} 🔥"
    
    @staticmethod
    def chinese_elegant(text):
        """صيني أنيق - بأحرف صينية فاخرة"""
        base = ChineseFonts.chinese_standard(text)
        return f"✨ {base} ✨"
    
    @staticmethod
    def chinese_double(text):
        """صيني مزدوج - بأقواس"""
        base = ChineseFonts.chinese_standard(text)
        return f"『{base}』"
    
    @staticmethod
    def chinese_with_heart(text):
        """صيني بقلوب"""
        base = ChineseFonts.chinese_standard(text)
        return f"♡ {base} ♡"
    
    @staticmethod
    def chinese_with_star(text):
        """صيني بنجوم"""
        base = ChineseFonts.chinese_standard(text)
        return f"★ {base} ★"
    
    @staticmethod
    def chinese_vertical(text):
        """صيني عمودي - كتابة عمودية"""
        base = ChineseFonts.chinese_standard(text)
        return "\n".join(base)

# قائمة الخطوط الصينية
CHINESE_STYLES = [
    {"name": "صيني قياسي", "func": ChineseFonts.chinese_standard, "emoji": "🇨🇳", "desc": "ترجمة صينية مبسطة"},
    {"name": "صيني تقليدي", "func": ChineseFonts.chinese_traditional, "emoji": "🏮", "desc": "ترجمة صينية تقليدية"},
    {"name": "صيني لطيف", "func": ChineseFonts.chinese_cute, "emoji": "🌸", "desc": "صيني بأسلوب لطيف"},
    {"name": "صيني كول", "func": ChineseFonts.chinese_cool, "emoji": "🔥", "desc": "صيني بأسلوب جريء"},
    {"name": "صيني أنيق", "func": ChineseFonts.chinese_elegant, "emoji": "✨", "desc": "صيني بأسلوب فاخر"},
    {"name": "صيني مزدوج", "func": ChineseFonts.chinese_double, "emoji": "📦", "desc": "صيني بأقواس مزدوجة"},
    {"name": "صيني بقلوب", "func": ChineseFonts.chinese_with_heart, "emoji": "❤️", "desc": "صيني مزخرف بقلوب"},
    {"name": "صيني بنجوم", "func": ChineseFonts.chinese_with_star, "emoji": "⭐", "desc": "صيني مزخرف بنجوم"},
    {"name": "صيني عمودي", "func": ChineseFonts.chinese_vertical, "emoji": "📜", "desc": "كتابة صينية عمودية"},
]