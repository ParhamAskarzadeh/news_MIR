import re
from hazm import Normalizer


class SelfNormalizer:
    def __init__(self):
        self.normalizer = Normalizer()

    def remove_shapes_and_convert_emojis_to_unicode(self, text: str):
        shape_list = re.findall(r'[^\w\s,]', text)  # find all shape and emojis
        for shape in shape_list:
            shape_code = shape.encode('unicode-escape').decode('ASCII')
            if 'U000' in shape_code:  # if the shape is an emoji
                text = text.replace(shape, ' {} '.format(shape_code))
            else:
                text = text.replace(shape, ' ')
        return text

    def character_replacer(self, text: str):
        # Numbers
        text = re.sub(r'[٠⓪⓿０𝟶🄌]', '۰', text)
        text = re.sub(r'[١⓵❶➀➊꘡]', '۱', text)
        text = re.sub(r'[٢②２𝟐]', '۲', text)
        text = re.sub(r'[٣③３𝟛]', '۳', text)
        text = re.sub(r'[٤۴⓸➍𝟒𝟜]', '۴', text)
        text = re.sub(r'[٥⓹❺５𝟝]', '۵', text)
        text = re.sub(r'[٦۶⑥❻６𝟞𝟨]', '۶', text)
        text = re.sub(r'[٧➆➐７𝟟]', '۷', text)
        text = re.sub(r'[٨⑧❽８𝟖]', '۸', text)
        text = re.sub(r'[٩⑨❾𝟗]', '۹', text)

        # Alphabet
        text = re.sub(r'[آأ𞸀]', 'ا', text)
        text = re.sub(r'[بﭒﭓﭔﭕ𞸁]', 'ب', text)
        text = re.sub(r'[ﭗﭘﭙ]', 'پ', text)
        text = re.sub(r'[تﺖﭧ𞸕]', 'ت', text)
        text = re.sub(r'[ثﺙﺚ𞸶𞸖]', 'ث', text)
        text = re.sub(r'[ﺝﺞﺠ𞸢𞸂]', 'ج', text)
        text = re.sub(r'[چﭻﭼﮀ]', 'چ', text)
        text = re.sub(r'[حﺢﺣ𞸇]', 'ح', text)
        text = re.sub(r'[ﺦﺨ𞸗]', 'خ', text)

        text = re.sub(r'[دﺩﺪ]', 'د', text)
        text = re.sub(r'[ذﺫﺬ𞸘]', 'ذ', text)

        text = re.sub(r'[رﺭﺮ𞸓]', 'ر', text)
        text = re.sub(r'[زࢲﺯﺰ𞸆]', 'ز', text)
        text = re.sub(r'[ژﮊﮋ]', 'ژ', text)
        text = re.sub(r'[ﺱﺳﺴ𞸎𞸮]', 'س', text)
        text = re.sub(r'[ﺵﺶﺸ𞸴𞸔]', 'ش', text)
        text = re.sub(r'[ص𞸱𞸑]', 'ص', text)
        text = re.sub(r'[ضﻀ𞸹𞸙]', 'ض', text)
        text = re.sub(r'[ﻂﻃ𞸈]', 'ط', text)
        text = re.sub(r'[ﻆ𞸚]', 'ظ', text)
        text = re.sub(r'[عﻉﻊﻌ𞸯𞸏]', 'ع', text)
        text = re.sub(r'[ﻎﻏﻐ𞸻𞸛]', 'غ', text)
        text = re.sub(r'[ف𞸞𞸐]', 'ف', text)
        text = re.sub(r'[ﻖﻘ𞸟𞸒]', 'ق', text)
        text = re.sub(r'[گﮓﮔﮕ]', 'گ', text)
        text = re.sub(r'[كﮑ𞸊𞸪]', 'ک', text)
        text = re.sub(r'[ﻝﻞﻟ𞸋]', 'ل', text)
        text = re.sub(r'[مﻡﻤ𞸬𞸌]', 'م', text)
        text = re.sub(r'[ﻥ𞸍𞸭]', 'ن', text)
        text = re.sub(r'[ﻭﻮ𞸅ۅﯠ]', 'و', text)
        text = text.replace('وو', 'و')
        text = re.sub(r'[هﮪﻪ𞸤ﻫﻬ]', 'ه', text)
        text = re.sub(r'[ةﺔ]', 'ه', text)
        text = re.sub(r'[ىﻯﻰ𞸉ﯨﯩ]', 'ی', text)
        text = text.replace('ئی', 'یی')
        text = re.sub(r'[ئﺉﺋ]', 'ئ', text)
        text = re.sub(r'[ءﺀ۽]', 'ء', text)
        text = text.replace('﷼', ' ریال ')

        text = text.replace(' می ', ' می\u200c')
        text = text.replace(' نمی ', ' نمی\u200c')
        text = text.replace(' برمی ', ' برمی\u200c')
        text = text.replace(' برنمی ', ' برنمی\u200c')

        # Whitespace
        text = re.sub(r'(\r|\f|\v|\\r|\\n)+', '\n', text)
        text = re.sub(r'\s?\n\s+', '\n', text)
        text = re.sub(r'[\t]+', ' ', text)
        text = re.sub(r' {2,}', ' ', text)

        # semi-space
        text = text.replace('&zwnj;', '\u200c')
        text = re.sub(r'[\u2000-\u200f]+', "\u200c", text)
        return text

    def normalize_with_hazm(self, text: str):
        return self.normalizer.normalize(text)

    def complete_normalize(self, text: str) -> str:
        text = self.remove_shapes_and_convert_emojis_to_unicode(text)
        text = self.character_replacer(text)
        text = self.normalizer.normalize(text)

        return text.strip()
