import re

CAMEL_PATTERN_1 = re.compile('(.)([A-Z][a-z]+)')
CAMEL_PATTERN_2 = re.compile('([a-z0-9])([A-Z])')

NON_ALPHANUM_PATTERN = re.compile('[^a-zA-Z]')

DATE_PATTERNS = [re.compile('([0-9]{4})[\\.\\/\\-]([0-9]{1,2})[\\.\\/\\-]([0-9]{1,2})'),
                 re.compile(
                     '^(?=\\d)(?:(?!(?:(?:0?[5-9]|1[0-4])(?:\\.|-|\\/)10(?:\\.|-|\\/)(?:1582))|(?:(?:0?[3-9]|1[0-3])(?:\\.|-|\\/)0?9(?:\\.|-|\\/)(?:1752)))(31(?!(?:\\.|-|\\/)(?:0?[2469]|11))|30(?!(?:\\.|-|\\/)0?2)|(?:29(?:(?!(?:\\.|-|\\/)0?2(?:\\.|-|\\/))|(?=\\D0?2\\D(?:(?!000[04]|(?:(?:1[^0-6]|[2468][^048]|[3579][^26])00))(?:(?:(?:\\d\\d)(?:[02468][048]|[13579][26])(?!\\x20BC))|(?:00(?:42|3[0369]|2[147]|1[258]|09)\\x20BC))))))|2[0-8]|1\\d|0?[1-9])([-.\\/])(1[012]|(?:0?[1-9]))\\2((?=(?:00(?:4[0-5]|[0-3]?\\d)\\x20BC)|(?:\\d{4}(?:$|(?=\\x20\\d)\\x20)))\\d{4}(?:\\x20BC)?)(?:$|(?=\\x20\\d)\\x20))?((?:(?:0?[1-9]|1[012])(?::[0-5]\\d){0,2}(?:\\x20[aApP][mM]))|(?:[01]\\d|2[0-3])(?::[0-5]\\d){1,2})?$'),
                 re.compile(
                     '^(?:(?:(?:(?:(?:1[6-9]|[2-9]\\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(\\/|-|\\.)(?:0?2\\1(?:29)))|(?:(?:(?:1[6-9]|[2-9]\\d)?\\d{2})(\\/|-|\\.)(?:(?:(?:0?[13578]|1[02])\\2(?:31))|(?:(?:0?[1,3-9]|1[0-2])\\2(29|30))|(?:(?:0?[1-9])|(?:1[0-2]))\\2(?:0?[1-9]|1\\d|2[0-8]))))$'),
                 re.compile(
                     '^(((0?[1-9]|[12]\\d|3[01])[\\.\\-\\/](0?[13578]|1[02])[\\.\\-\\/]((1[6-9]|[2-9]\\d)?\\d{2}))|((0?[1-9]|[12]\\d|30)[\\.\\-\\/](0?[13456789]|1[012])[\\.\\-\\/]((1[6-9]|[2-9]\\d)?\\d{2}))|((0?[1-9]|1\\d|2[0-8])[\\.\\-\\/]0?2[\\.\\-\\/]((1[6-9]|[2-9]\\d)?\\d{2}))|(29[\\.\\-\\/]0?2[\\.\\-\\/]((1[6-9]|[2-9]\\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)|00)))$'),
                 re.compile('^([0]?[1-9]|[1][0-2])[./-]([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0-9]{4}|[0-9]{2})$')]


def _camel_to_white(label):
    label = CAMEL_PATTERN_1.sub(r'\1 \2', label)
    return CAMEL_PATTERN_2.sub(r'\1 \2', label)


def check_for_and_remove_dates(li: list):
    res = []
    for item in li:
        for pattern in DATE_PATTERNS:
            if pattern.search(item):
                print('found date')
                continue
            else:
                res.append(item)
    return res


def check_for_date(att):
    for pattern in DATE_PATTERNS:
        if pattern.search(att):
            return True
    return False


def preprocess_label(label):
    label = str(label)
    label = _camel_to_white(label).lower()
    label = NON_ALPHANUM_PATTERN.sub(' ', label)
    parts = label.split()
    res = []
    for part in parts:
        clean = ''.join([i for i in part if not i.isdigit()])
        res.append(clean)
    return ' '.join(res)


def clean_attribute_name(att_name):
    return preprocess_label(att_name).replace('case', '').lower().strip()
