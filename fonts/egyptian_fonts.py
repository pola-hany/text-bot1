class EgyptianFonts:
    """خطوط هيروغليفية مصرية قديمة"""
    
    @staticmethod
    def hieroglyphic(text):
        """هيروغليفي مصري - رموز مصرية قديمة"""
        hieroglyph_map = {
            # حروف عربية
            'ا': '𓄿',  # ibis
            'ب': '𓃀',  # foot
            'ت': '𓏏',  # bread
            'ث': '𓐍',  # placenta
            'ج': '𓂧',  # hand
            'ح': '𓎛',  # wick
            'خ': '𓐍',  # placenta
            'د': '𓂧',  # hand
            'ذ': '𓂻',  # arm
            'ر': '𓂋',  # mouth
            'ز': '𓊃',  # door bolt
            'س': '𓊃',  # door bolt
            'ش': '𓈙',  # pool
            'ص': '𓊃',  # door bolt
            'ض': '𓂧',  # hand
            'ط': '𓍿',  # tether
            'ظ': '𓍿',  # tether
            'ع': '𓂝',  # arm
            'غ': '𓎛',  # wick
            'ف': '𓆑',  # horned viper
            'ق': '𓐍',  # placenta
            'ك': '𓎡',  # basket
            'ل': '𓃭',  # lion
            'م': '𓅓',  # owl
            'ن': '𓈖',  # water
            'ه': '𓎛',  # wick
            'و': '𓅱',  # quail chick
            'ي': '𓇋',  # reed
            'ء': '𓄿',  # ibis
            'ؤ': '𓅱',  # quail
            'ئ': '𓇋',  # reed
            'آ': '𓄿',  # ibis
            
            # حروف إنجليزية
            'a': '𓄿', 'b': '𓃀', 'c': '𓎡', 'd': '𓂧', 'e': '𓇋', 'f': '𓆑',
            'g': '𓎛', 'h': '𓎛', 'i': '𓇋', 'j': '𓂧', 'k': '𓎡', 'l': '𓃭',
            'm': '𓅓', 'n': '𓈖', 'o': '𓅱', 'p': '𓊪', 'q': '𓐍', 'r': '𓂋',
            's': '𓊃', 't': '𓏏', 'u': '𓅱', 'v': '𓆑', 'w': '𓅱', 'x': '𓎡𓊃',
            'y': '𓇋', 'z': '𓊃'
        }
        
        result = ""
        for char in text:
            if char in hieroglyph_map:
                result += hieroglyph_map[char]
            elif char.lower() in hieroglyph_map:
                result += hieroglyph_map[char.lower()]
            else:
                result += char
        return result
    
    @staticmethod
    def hieroglyphic_royal(text):
        """هيروغليفي ملكي - بأحرف ملكية"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓋴 {base} 𓋴"  # Sedge for royalty
    
    @staticmethod
    def hieroglyphic_golden(text):
        """هيروغليفي ذهبي - برموز ذهبية"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓋞 {base} 𓋞"  # Gold sign
    
    @staticmethod
    def hieroglyphic_papyrus(text):
        """هيروغليفي بردية - بأسلوب البرديات"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓇅 {base} 𓇅"  # Papyrus roll
    
    @staticmethod
    def hieroglyphic_ankh(text):
        """هيروغليفي أنخ - برمز الحياة"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓋹 {base} 𓋹"  # Ankh
    
    @staticmethod
    def hieroglyphic_eye(text):
        """هيروغليفي عين حورس"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓂀 {base} 𓂀"  # Eye of Horus
    
    @staticmethod
    def hieroglyphic_scarab(text):
        """هيروغليفي جعران - برمز الجعران"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓐍𓂋𓃀𓆣 {base} 𓆣𓃀𓂋𓐍"  # Scarab
    
    @staticmethod
    def hieroglyphic_temple(text):
        """هيروغليفي معبد - بأسلوب المعابد"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓉐 {base} 𓉐"  # Temple
    
    @staticmethod
    def hieroglyphic_pyramid(text):
        """هيروغليفي هرمي"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓍋 {base} 𓍋"  # Pyramid
    
    @staticmethod
    def hieroglyphic_cartouche(text):
        """هيروغليفي خرطوش - داخل خرطوش ملكي"""
        base = EgyptianFonts.hieroglyphic(text)
        return f"𓋴𓈖𓊹 {base} 𓊹𓈖𓋴"  # Cartouche style

# قائمة الخطوط المصرية القديمة
EGYPTIAN_STYLES = [
    {"name": "هيروغليفي", "func": EgyptianFonts.hieroglyphic, "emoji": "𓂀", "desc": "رموز مصرية قديمة"},
    {"name": "هيروغليفي ملكي", "func": EgyptianFonts.hieroglyphic_royal, "emoji": "𓋴", "desc": "بأحرف ملكية"},
    {"name": "هيروغليفي ذهبي", "func": EgyptianFonts.hieroglyphic_golden, "emoji": "𓋞", "desc": "برموز ذهبية"},
    {"name": "هيروغليفي بردية", "func": EgyptianFonts.hieroglyphic_papyrus, "emoji": "𓇅", "desc": "بأسلوب البرديات"},
    {"name": "هيروغليفي أنخ", "func": EgyptianFonts.hieroglyphic_ankh, "emoji": "𓋹", "desc": "برمز الحياة"},
    {"name": "هيروغليفي عين حورس", "func": EgyptianFonts.hieroglyphic_eye, "emoji": "𓂀", "desc": "برمز عين حورس"},
    {"name": "هيروغليفي جعران", "func": EgyptianFonts.hieroglyphic_scarab, "emoji": "𓆣", "desc": "برمز الجعران المقدس"},
    {"name": "هيروغليفي معبد", "func": EgyptianFonts.hieroglyphic_temple, "emoji": "𓉐", "desc": "بأسلوب المعابد"},
    {"name": "هيروغليفي هرمي", "func": EgyptianFonts.hieroglyphic_pyramid, "emoji": "𓍋", "desc": "بأسلوب الأهرامات"},
    {"name": "هيروغليفي خرطوش", "func": EgyptianFonts.hieroglyphic_cartouche, "emoji": "𓋴𓈖𓊹", "desc": "داخل خرطوش ملكي"},
]