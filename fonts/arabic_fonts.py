class ArabicFonts:
    """خطوط عربية حديثة وشبابية - مستوحاة من أحدث التصاميم"""
    
    # ============= خطوط كلاسيكية أنيقة =============
    
    @staticmethod
    def amiri(text):
        """أميري - خط نسخي كلاسيكي أنيق"""
        return f"<b>{text}</b>"
    
    @staticmethod
    def noto_naskh(text):
        """نوتو نسخ - خط واضح عصري"""
        return f"<i>{text}</i>"
    
    @staticmethod
    def scheherazade(text):
        """شهرزاد - خط مستوحى من المخطوطات"""
        return f"<u>{text}</u>"
    
    # ============= خطوط ديوانية وثلثية =============
    
    @staticmethod
    def diwani(text):
        """ديواني - خط منحني أنيق"""
        diwani_map = {
            'ا': 'ﺍ', 'ب': 'ﺏ', 'ت': 'ﺕ', 'ث': 'ﺙ', 'ج': 'ﺝ', 'ح': 'ﺡ',
            'خ': 'ﺥ', 'د': 'ﺩ', 'ذ': 'ﺫ', 'ر': 'ﺭ', 'ز': 'ﺯ', 'س': 'ﺱ',
            'ش': 'ﺵ', 'ص': 'ﺹ', 'ض': 'ﺽ', 'ط': 'ﻁ', 'ظ': 'ﻅ', 'ع': 'ﻉ',
            'غ': 'ﻍ', 'ف': 'ﻑ', 'ق': 'ﻕ', 'ك': 'ﻙ', 'ل': 'ﻝ', 'م': 'ﻡ',
            'ن': 'ﻥ', 'ه': 'ﻩ', 'و': 'ﻭ', 'ي': 'ﻱ'
        }
        result = ""
        for char in text:
            if char in diwani_map:
                result += diwani_map[char]
            else:
                result += char
        return f"<b>{result}</b>"
    
    @staticmethod
    def thuluth(text):
        """ثلث - خط زخرفي فني"""
        thuluth_map = {
            'ا': 'ﭐ', 'ب': 'ﭒ', 'ت': 'ﭞ', 'ث': 'ﭪ', 'ج': 'ﭺ', 'ح': 'ﲊ',
            'خ': 'ﲔ', 'د': 'ﺩ', 'ذ': 'ﺫ', 'ر': 'ﺭ', 'ز': 'ﺯ', 'س': 'ﺱ',
            'ش': 'ﺵ', 'ص': 'ﺹ', 'ض': 'ﺽ', 'ط': 'ﻁ', 'ظ': 'ﻅ', 'ع': 'ﻉ',
            'غ': 'ﻍ', 'ف': 'ﻑ', 'ق': 'ﻕ', 'ك': 'ﻙ', 'ل': 'ﻝ', 'م': 'ﻡ',
            'ن': 'ﻥ', 'ه': 'ﻩ', 'و': 'ﻭ', 'ي': 'ﻱ'
        }
        result = ""
        for char in text:
            if char in thuluth_map:
                result += thuluth_map[char]
            else:
                result += char
        return f"<i>{result}</i>"
    
    @staticmethod
    def farisi(text):
        """فارسي - خط نستعليق أنيق"""
        farisi_map = {
            'ا': 'آ', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ک', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ی'
        }
        result = ""
        for char in text:
            if char in farisi_map:
                result += farisi_map[char]
            else:
                result += char
        return f"<b>{result}</b>"
    
    # ============= خطوط حديثة وشبابية =============
    
    @staticmethod
    def jomhuria(text):
        """جمهورية - خط عريض قوي مستوحى من الخط العربي [citation:1]"""
        # خط ثقيل الوزن، مثالي للعناوين
        jomhuria_map = {
            'ا': 'ﺍ', 'ب': 'ﺏ', 'ت': 'ﺕ', 'ث': 'ﺙ', 'ج': 'ﺝ', 'ح': 'ﺡ',
            'خ': 'ﺥ', 'د': 'ﺩ', 'ذ': 'ﺫ', 'ر': 'ﺭ', 'ز': 'ﺯ', 'س': 'ﺱ',
            'ش': 'ﺵ', 'ص': 'ﺹ', 'ض': 'ﺽ', 'ط': 'ﻁ', 'ظ': 'ﻅ', 'ع': 'ﻉ',
            'غ': 'ﻍ', 'ف': 'ﻑ', 'ق': 'ﻕ', 'ك': 'ﻙ', 'ل': 'ﻝ', 'م': 'ﻡ',
            'ن': 'ﻥ', 'ه': 'ﻩ', 'و': 'ﻭ', 'ي': 'ﻱ'
        }
        result = ""
        for char in text:
            if char in jomhuria_map:
                result += jomhuria_map[char]
            else:
                result += char
        return f"<b><big>{result}</big></b>"
    
    @staticmethod
    def qebica(text):
        """قبيقة - خط slab serif عربي بلمسة عصرية [citation:7]"""
        # خط slab serif مميز، يجمع بين الحداثة والطابع العربي
        qebica_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in qebica_map:
                result += qebica_map[char]
            else:
                result += char
        return f"<code>{result}</code>"
    
    @staticmethod
    def cordoba(text):
        """قرطبة - خط كوفي متغير عصري [citation:8]"""
        # مستوحى من خط المصحف الكوفي مع لمسة عصرية
        cordoba_map = {
            'ا': '𐤀', 'ب': '𐤁', 'ت': '𐤕', 'ث': '𐤔', 'ج': '𐤉',
            'ح': '𐤇', 'خ': '𐤊', 'د': '𐤃', 'ذ': '𐤆', 'ر': '𐤓',
            'ز': '𐤆', 'س': '𐤔', 'ش': '𐤔', 'ص': '𐤑', 'ض': '𐤃',
            'ط': '𐤈', 'ظ': '𐤆', 'ع': '𐤏', 'غ': '𐤂', 'ف': '𐤐',
            'ق': '𐤒', 'ك': '𐤊', 'ل': '𐤋', 'م': '𐤌', 'ن': '𐤍',
            'ه': '𐤄', 'و': '𐤅', 'ي': '𐤉'
        }
        result = ""
        for char in text:
            if char in cordoba_map:
                result += cordoba_map[char]
            else:
                result += char
        return f"<code>{result}</code>"
    
    @staticmethod
    def sketsa_ramadhan(text):
        """سكتسا رمضان - خط عربي مستوحى من خط النسخ [citation:10]"""
        # خط عربي بتصميم عصري مناسب للتصاميم الإسلامية
        sketsa_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in sketsa_map:
                result += sketsa_map[char]
            else:
                result += char
        return f"<i>{result}</i>"
    
    # ============= خطوط كوفية هندسية =============
    
    @staticmethod
    def kufic(text):
        """كوفي هندسي - خط زخرفي قديم"""
        kufi_map = {
            'ا': '𐤀', 'ب': '𐤁', 'ت': '𐤕', 'ث': '𐤔', 'ج': '𐤉',
            'ح': '𐤇', 'خ': '𐤊', 'د': '𐤃', 'ذ': '𐤆', 'ر': '𐤓',
            'ز': '𐤆', 'س': '𐤔', 'ش': '𐤔', 'ص': '𐤑', 'ض': '𐤃',
            'ط': '𐤈', 'ظ': '𐤆', 'ع': '𐤏', 'غ': '𐤂', 'ف': '𐤐',
            'ق': '𐤒', 'ك': '𐤊', 'ل': '𐤋', 'م': '𐤌', 'ن': '𐤍',
            'ه': '𐤄', 'و': '𐤅', 'ي': '𐤉'
        }
        result = ""
        for char in text:
            if char in kufi_map:
                result += kufi_map[char]
            else:
                result += char
        return f"<code>{result}</code>"
    
    @staticmethod
    def noto_kufi(text):
        """نوتو كوفي - خط كوفي هندسي حديث [citation:5]"""
        # من مجموعة Noto، تصميم هندسي نظيف
        noto_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in noto_map:
                result += noto_map[char]
            else:
                result += char
        return f"<b>{result}</b>"
    
    # ============= خطوط بخط الرقعة واليدوية =============
    
    @staticmethod
    def ruqaa(text):
        """رقعة - خط واضح وسريع"""
        ruqaa_map = {
            'ا': 'ﺍ', 'ب': 'ﺑ', 'ت': 'ﺗ', 'ث': 'ﺛ', 'ج': 'ﺟ', 'ح': 'ﺣ',
            'خ': 'ﺧ', 'د': 'ﺩ', 'ذ': 'ﺫ', 'ر': 'ﺭ', 'ز': 'ﺯ', 'س': 'ﺳ',
            'ش': 'ﺷ', 'ص': 'ﺻ', 'ض': 'ﺿ', 'ط': 'ﻃ', 'ظ': 'ﻇ', 'ع': 'ﻋ',
            'غ': 'ﻏ', 'ف': 'ﻓ', 'ق': 'ﻗ', 'ك': 'ﻛ', 'ل': 'ﻟ', 'م': 'ﻣ',
            'ن': 'ﻧ', 'ه': 'ﻫ', 'و': 'ﻭ', 'ي': 'ﻳ'
        }
        result = ""
        for char in text:
            if char in ruqaa_map:
                result += ruqaa_map[char]
            else:
                result += char
        return result
    
    @staticmethod
    def aref_ruqaa(text):
        """عارف رقعة - خط رقعة عصري [citation:5]"""
        # خط رقعة بتصميم حديث للعناوين
        aref_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in aref_map:
                result += aref_map[char]
            else:
                result += char
        return f"<i>{result}</i>"
    
    # ============= خطوط مغاربية وأندلسية =============
    
    @staticmethod
    def andalus(text):
        """أندلسي - خط مغربي أنيق"""
        andalus_map = {
            'ا': 'ا', 'ب': 'ڀ', 'ت': 'ٺ', 'ث': 'ٿ', 'ج': 'ڃ', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ڢ', 'ق': 'ڧ', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in andalus_map:
                result += andalus_map[char]
            else:
                result += char
        return f"<i>{result}</i>"
    
    @staticmethod
    def maghribi(text):
        """مغربي - خط شمال أفريقيا"""
        maghribi_map = {
            'ا': 'ا', 'ب': 'ڀ', 'ت': 'ٺ', 'ث': 'ٿ', 'ج': 'ڃ', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ڢ', 'ق': 'ڧ', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in maghribi_map:
                result += maghribi_map[char]
            else:
                result += char
        return result
    
    # ============= خطوط عصرية بلمسات شبابية =============
    
    @staticmethod
    def modern(text):
        """عصري - تصميم حديث جريء"""
        modern_map = {
            'ا': 'ا', 'ب': 'ٻ', 'ت': 'ٹ', 'ث': 'ٺ', 'ج': 'چ', 'ح': 'ځ',
            'خ': 'څ', 'د': 'ڈ', 'ذ': 'ڎ', 'ر': 'ڕ', 'ز': 'ڒ', 'س': 'ښ',
            'ش': 'ڜ', 'ص': 'ڞ', 'ض': 'ڠ', 'ط': 'ڡ', 'ظ': 'ڣ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ڦ', 'ق': 'ڨ', 'ك': 'ک', 'ل': 'ل', 'م': 'م',
            'ن': 'ڻ', 'ه': 'ھ', 'و': 'ۋ', 'ي': 'ێ'
        }
        result = ""
        for char in text:
            if char in modern_map:
                result += modern_map[char]
            else:
                result += char
        return f"<b>{result}</b>"
    
    @staticmethod
    def el_messiri(text):
        """المصيري - خط عربي عالي التباين [citation:5]"""
        # خط عالي التباين مناسب للعناوين
        messiri_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in messiri_map:
                result += messiri_map[char]
            else:
                result += char
        return f"<b><big>{result}</big></b>"
    
    @staticmethod
    def cairo(text):
        """قاهرة - خط عربي sans-serif عصري [citation:5]"""
        # خط sans-serif حديث
        cairo_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in cairo_map:
                result += cairo_map[char]
            else:
                result += char
        return result
    
    @staticmethod
    def tajawal(text):
        """تجاوب - خط عربي حديث بلمسات كوفية [citation:5]"""
        # خط عصري بتصميم هندسي
        tajawal_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in tajawal_map:
                result += tajawal_map[char]
            else:
                result += char
        return f"<i>{result}</i>"
    
    # ============= خطوط مزخرفة بعلامات ونقاط =============
    
    @staticmethod
    def dotted(text):
        """منقط - خط مع نقاط زخرفية"""
        dotted_map = {
            'ا': 'ا', 'ب': 'ۻ', 'ت': 'ۼ', 'ث': '۽', 'ج': '۾', 'ح': 'ۿ',
            'خ': 'ݗ', 'د': 'ݚ', 'ذ': 'ݛ', 'ر': 'ݜ', 'ز': 'ݝ', 'س': 'ݞ',
            'ش': 'ݟ', 'ص': 'ݠ', 'ض': 'ݡ', 'ط': 'ݢ', 'ظ': 'ݣ', 'ع': 'ݤ',
            'غ': 'ݥ', 'ف': 'ݦ', 'ق': 'ݧ', 'ك': 'ݨ', 'ل': 'ݩ', 'م': 'ݪ',
            'ن': 'ݫ', 'ه': 'ݬ', 'و': 'ݭ', 'ي': 'ݮ'
        }
        result = ""
        for char in text:
            if char in dotted_map:
                result += dotted_map[char]
            else:
                result += char
        return f"✨ {result} ✨"
    
    @staticmethod
    def swashed(text):
        """مزخرف - خط مع لمسات زخرفية"""
        swashed_map = {
            'ا': 'آ', 'ب': 'ٻ', 'ت': 'ټ', 'ث': 'ٽ', 'ج': 'چ', 'ح': 'ځ',
            'خ': 'څ', 'د': 'ډ', 'ذ': 'ڊ', 'ر': 'ړ', 'ز': 'ږ', 'س': 'ښ',
            'ش': 'ڜ', 'ص': 'ڞ', 'ض': 'ڠ', 'ط': 'ڡ', 'ظ': 'ڣ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ڦ', 'ق': 'ڨ', 'ك': 'ک', 'ل': 'ل', 'م': 'م',
            'ن': 'ڻ', 'ه': 'ھ', 'و': 'ۋ', 'ي': 'ێ'
        }
        result = ""
        for char in text:
            if char in swashed_map:
                result += swashed_map[char]
            else:
                result += char
        return f"꧁{result}꧂"
    
    @staticmethod
    def floral(text):
        """زهرة - خط بنقوش زهرية"""
        floral_map = {
            'ا': '۞', 'ب': '۩', 'ت': '۪', 'ث': '۫', 'ج': '۬', 'ح': 'ۭ',
            'خ': 'ۮ', 'د': 'ۯ', 'ذ': '۰', 'ر': '۱', 'ز': '۲', 'س': '۳',
            'ش': '۴', 'ص': '۵', 'ض': '۶', 'ط': '۷', 'ظ': '۸', 'ع': '۹',
            'غ': '۱۰', 'ف': '؋', 'ق': '،', 'ك': '؍', 'ل': '؎', 'م': '؏',
            'ن': 'ؐ', 'ه': 'ؑ', 'و': 'ؒ', 'ي': 'ؓ'
        }
        result = ""
        for char in text:
            if char in floral_map:
                result += floral_map[char]
            else:
                result += char
        return f"🌸 {result} 🌸"
    
    @staticmethod
    def double_letter(text):
        """مكرر - حروف مزدوجة"""
        result = ""
        for char in text:
            result += char + char
        return f"🔁 {result}"
    
    @staticmethod
    def mirrored(text):
        """معكوس - نص مقلوب"""
        return text[::-1]
    
    @staticmethod
    def spaced(text):
        """متباعد - مسافات بين الحروف"""
        return " ".join(text)
    
    @staticmethod
    def zalzalah(text):
        """زلزلة - خط مائل ديناميكي"""
        zalzalah_map = {
            'ا': 'ا', 'ب': 'ب', 'ت': 'ت', 'ث': 'ث', 'ج': 'ج', 'ح': 'ح',
            'خ': 'خ', 'د': 'د', 'ذ': 'ذ', 'ر': 'ر', 'ز': 'ز', 'س': 'س',
            'ش': 'ش', 'ص': 'ص', 'ض': 'ض', 'ط': 'ط', 'ظ': 'ظ', 'ع': 'ع',
            'غ': 'غ', 'ف': 'ف', 'ق': 'ق', 'ك': 'ك', 'ل': 'ل', 'م': 'م',
            'ن': 'ن', 'ه': 'ه', 'و': 'و', 'ي': 'ي'
        }
        result = ""
        for char in text:
            if char in zalzalah_map:
                result += zalzalah_map[char]
            else:
                result += char
        return f"<i>{result}</i>"


# ============= قائمة الخطوط العربية الكاملة مع وصف =============

ARABIC_FONTS = [
    # خطوط كلاسيكية
    {"name": "أميري", "func": ArabicFonts.amiri, "emoji": "📜", "desc": "خط نسخي كلاسيكي أنيق"},
    {"name": "ديواني", "func": ArabicFonts.diwani, "emoji": "🖋️", "desc": "خط منحني أنيق"},
    {"name": "ثلث", "func": ArabicFonts.thuluth, "emoji": "🎨", "desc": "خط زخرفي فني"},
    {"name": "فارسي", "func": ArabicFonts.farisi, "emoji": "🇮🇷", "desc": "خط نستعليق أنيق"},
    {"name": "رقعة", "func": ArabicFonts.ruqaa, "emoji": "✍️", "desc": "خط واضح وسريع"},
    
    # خطوط حديثة وقوية
    {"name": "جمهورية", "func": ArabicFonts.jomhuria, "emoji": "💪", "desc": "خط عريض قوي [citation:1]"},
    {"name": "قبيقة", "func": ArabicFonts.qebica, "emoji": "🔲", "desc": "خط slab serif عصري [citation:7]"},
    {"name": "قرطبة", "func": ArabicFonts.cordoba, "emoji": "🏛️", "desc": "خط كوفي متغير [citation:8]"},
    {"name": "كوفي هندسي", "func": ArabicFonts.kufic, "emoji": "🔷", "desc": "خط هندسي زخرفي"},
    {"name": "نوتو كوفي", "func": ArabicFonts.noto_kufi, "emoji": "📐", "desc": "كوفي هندسي نظيف [citation:5]"},
    
    # خطوط مغاربية
    {"name": "أندلسي", "func": ArabicFonts.andalus, "emoji": "🇪🇸", "desc": "خط مغربي أنيق"},
    {"name": "مغربي", "func": ArabicFonts.maghribi, "emoji": "🌴", "desc": "خط شمال أفريقيا"},
    
    # خطوط عصرية وشبابية
    {"name": "عصري", "func": ArabicFonts.modern, "emoji": "💎", "desc": "تصميم حديث جريء"},
    {"name": "المصيري", "func": ArabicFonts.el_messiri, "emoji": "🎯", "desc": "خط عالي التباين [citation:5]"},
    {"name": "قاهرة", "func": ArabicFonts.cairo, "emoji": "🏙️", "desc": "خط sans-serif عصري [citation:5]"},
    {"name": "تجاوب", "func": ArabicFonts.tajawal, "emoji": "⚡", "desc": "خط كوفي عصري [citation:5]"},
    {"name": "سكتسا رمضان", "func": ArabicFonts.sketsa_ramadhan, "emoji": "🌙", "desc": "خط رمضاني [citation:10]"},
    {"name": "عارف رقعة", "func": ArabicFonts.aref_ruqaa, "emoji": "📝", "desc": "خط رقعة عصري [citation:5]"},
    
    # خطوط مزخرفة
    {"name": "منقط", "func": ArabicFonts.dotted, "emoji": "⚫", "desc": "خط بنقاط زخرفية"},
    {"name": "مزخرف", "func": ArabicFonts.swashed, "emoji": "🎭", "desc": "خط بلمسات زخرفية"},
    {"name": "زهرة", "func": ArabicFonts.floral, "emoji": "🌸", "desc": "خط بنقوش زهرية"},
    {"name": "مكرر", "func": ArabicFonts.double_letter, "emoji": "🔁", "desc": "حروف مزدوجة"},
    {"name": "معكوس", "func": ArabicFonts.mirrored, "emoji": "🔄", "desc": "نص مقلوب"},
    {"name": "متباعد", "func": ArabicFonts.spaced, "emoji": "␣", "desc": "مسافات بين الحروف"},
    {"name": "زلزلة", "func": ArabicFonts.zalzalah, "emoji": "🌊", "desc": "خط مائل ديناميكي"},
]