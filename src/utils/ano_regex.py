from datetime import datetime
from dateutil import parser
from dateutil.parser import ParserError
from itertools import product
import regex as re
import dill

with open('./data/first_names_trie_regex.pkl', 'rb') as f:
    first_trie_regex = dill.load(f)
with open('./data/last_names_trie_regex.pkl', 'rb') as f:
    last_trie_regex = dill.load(f)

COUNTRY_CODES_REGEX = r'41'
CURRENCY_REGEX = r'EUR|CHF|Fr\.|Franken|Francs'

def anonymize_regex(text, regex, by='ENTITY', start_tag='#', end_tag='#', count=True, first=1, compare_lowercase=False, keep_regex=False):
    """
    :param text:
    :param regex:
    :param by:
    :param start_tag:
    :param end_tag:
    :pram count:
    :param compare_lowercase:
    :param keep_regex:
    :return:
    """
    matches = list(re.finditer(re.compile(regex), text.lower() if compare_lowercase else text))
    replace_dict = {}
    counter = len(set(r.group() for r in matches)) + first - 1
    for r in matches[::-1]:
        replace_by = f'{start_tag}{by}_{counter}{end_tag}' if count else f'{start_tag}{by}{end_tag}'
        if r.group() not in replace_dict.keys():
            replace_dict.update({r.group(): replace_by}) 
            counter -=1
        text = f'{text[:r.span()[0]]}{replace_dict.get(r.group())}{text[r.span()[1]:]}'
    
    return {'text': text, 'replace_dict': replace_dict} | ({'regex': regex, 'matches': matches} if keep_regex else {})


def create_names_regex(names_list, boundary=r'\b'):
    """
    
    :param names_list:
    :return:
    """
    if isinstance(names_list, re.Pattern):
        return names_list
    return re.compile(boundary + '|'.join(sorted(list(set(n for n in names_list if len(n) > 0)), key=len, reverse=True)) + boundary)


def _update_result(result, new_result, keep_regex=False):
    """
    
    :param result:
    :param new_result:
    :param keep_regex:
    :return:
    """
    result.update({'text': new_result.get('text'), 'replace_dict': result.get('replace_dict') | new_result.get('replace_dict')})
    if keep_regex:
        result.update({'regex': result.get('regex') + [new_result.get('regex')], 'matches': result.get('matches') + new_result.get('matches')})
    return result


def _flip_replace_dict(replace_dict):
    """
    
    :param replace_dict:
    :return:
    """
    flipped_dict = {}
    for key, value in replace_dict.items():
        if value not in flipped_dict:
            flipped_dict[value] = {'matches': {key}, 'replacement': key}
        else:
            flipped_dict[value]['matches'].add(key)
            # Determine the replacement based on length and lexicographical order
            current_replacement = flipped_dict[value]['replacement']
            if len(key) > len(current_replacement) or (len(key) == len(current_replacement) and key < current_replacement):
                flipped_dict[value]['replacement'] = key
    return flipped_dict


def anonymize_ahv(text, by='AHVNR', start_tag='#', end_tag='#', count=True, first=1, keep_regex=False):
    """

    :param text:
    :param by:
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param keep_regex:
    :return:
    """
    regex = re.compile(r'\b756\.\s?\d{4}\.\s?\d{4}\.\s?\d{2}\b')
    return anonymize_regex(text, regex, by, start_tag, end_tag, count, first, False, keep_regex)


def anonymize_currency(text, by='CURRENCY', start_tag='#', end_tag='#', count=True, first=1, currency_regex=CURRENCY_REGEX,
                       separator_regex=r"'|’| ", decimal_regex=r"\.", without_symbol=True, compare_lowercase=False,
                       keep_regex=False):
    """
    :param text:
    :param by:
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param currency_regex:
    :param separator_regex:
    :param decimal_regex:
    :param without_symbol:
    :param compare_lowercase:
    :param keep_regex:
    :return:
    """
    sep = '(?:' + separator_regex + ')'
    num = r"(?:\d{1,3}(?:" + sep + r"?\d{1,3})*(?:" + decimal_regex + r"(?:\d{1,2}|-{1,2}|—{1,2}))?)"
    regex = (r"\b(?:(?:" + currency_regex + r")(?: )*-?" + num + r")" # '(?: )*' was '(?:\s)* '
             + r"|(?:-?" + num + "(?: )*(?:" + currency_regex + r")" # '(?: )*' was '(?:\s)* '
             + (r"|-?(?:" + num + sep + r")+" + num if without_symbol else "") + r")(\b)?")
    return anonymize_regex(text, re.compile(regex.lower() if compare_lowercase else regex), by, start_tag, end_tag, count, first,
                           compare_lowercase, keep_regex)


def anonymize_dates(text, by='DATE', start_tag='#', end_tag='#', count=True, first=1, lang='de', keep_regex=False):
    """
    :param text:
    :param date_dict:
    :param by:
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param lang:
    :param compare_lowercase:
    :return:
    """
    day = r'(0?[1-9]|[12][0-9]|3[01])'
    mon = r'(?:(\.|\/|-)(0?[1-9]|1[0-2])(\.|\/|-))'
    mon_lang = {'de': (r'(?:\.? ?([Jj]anuar|[Ff]ebruar|[Mm]ärz|[Aa]pril|[Mm]ai|[Jj]uni|[Jj]uli|[Aa]ugust|[Ss]eptember'
                       + r'|[Oo]ktober|[Nn]ovember|[Dd]ezember'
                       + r'|[Jj]an\.?|[Ff]eb\.?|[Mm]är\.?|[Aa]pr\.?|[Mm]ai\.?|[Jj]un\.?|[Jj]ul\.?|[Aa]ug\.?|[Ss]ep\.?'
                       + r'|[Oo]kt\.?|[Nn]ov\.?|[Dd]ez\.?))'),
                'fr': (r'(?:\.? ?([Jj]anvier|[Ff]évrier|[Mm]ars|[Aa]vril|[Mm]ai|[Jj]uin|[Jj]uillet|[Aa]oût|[Ss]eptembre'
                       + r'|[Oo]ctobre|[Nn]ovembre|[Dd]écembre'
                       + r'|[Jj]an\.?|[Ff]év\.?|[Mm]ar\.?|[Aa]vr\.?|[Jj]uil\.?|[Ss]ep\.?|[Oo]ct\.?'
                       + r'|[Nn]ov\.?|[Dd]éc\.?))'),
                'it': (r'(?:\.? ?([Gg]ennaio|[Ff]ebbraio|[Mm]arzo|[Aa]prile|[Mm]aggio|[Gg]iugno|[Ll]uglio|[Aa]gosto'
                       + r'|[Ss]ettembre|[Oo]ttobre|[Nn]ovembre|[Dd]icembre'
                       + r'|[Gg]en\.?|[Ff]eb\.?|[Mm]ar\.?|[Aa]pr\.?|[Mm]ag\.?|[Gg]iu\.?|[Ll]ug\.?'
                       + r'|[Aa]go\.?|[Ss]et\.?|[Oo]tt\.?|[Nn]ov\.?|[Dd]ic\.?))'),
                'en': (r'(?:\.? ?([Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust'
                       + r'|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember'
                       + r'|[Jj]an\.?|[Ff]eb\.?|[Mm]ar\.?|[Aa]pr\.?|[Mm]ay|[Jj]un\.?|[Jj]ul\.?|[Aa]ug\.?|[Ss]ep\.?'
                       +  r'|[Oo]ct\.?|[Nn]ov\.?|[Dd]ec\.?))')}
    mon_sub = {'jan': r'[Jj]anuar|[Jj]an\.?|[Jj]anvier|[Jj]an\.?|[Gg]ennaio|[Gg]en\.?',
               'feb': r'[Ff]ebruar|[Ff]eb\.?|[Ff]évrier|[Ff]év\.?|[Ff]ebbraio|feb\.?',
               'mar': r'[Mm]ärz|[Mm]Mär\.?|[Mm]ars|[Mm]ar\.?|[Mm]arzo|[Mm]ar\.?',
               'apr': r'[Aa]pril|[Aa]pr\.?|[Aa]vril|[Aa]vr\.?|[Aa]prile|[Aa]pr\.?',
               'may': r'[Mm]ai|[Mm]ai|[Mm]aggio',
               'jun': r'[Jj]uni|[Jj]un\.?|[Jj]uin|[Gg]iu\.?',
               'jul': r'[Jj]uli|[Jj]ul\.?|[Jj]uillet|[Ll]uglio|[Ll]ug\.?',
               'aug': r'[Aa]ugust|[Aa]ug\.?|[Aa]oût|[Aa]gosto|[Aa]go\.?',
               'sep': r'[Ss]eptember|[Ss]ep\.?|[Ss]eptembre|[Ss]ettembre|[Ss]et\.?',
               'oct': r'[Oo]ktober|[Oo]kt\.?|[Oo]ctobre|[Oo]ttobre|[Oo]tt\.?',
               'nov': r'[Nn]ovember|[Nn]ov\.?|[Nn]ovembre|[Nn]ov\.?',
               'dec': r'[Dd]ezember|[Dd]ez\.?|[Dd]écembre|[Dd]éc\.?|[Dd]icembre|[Dd]ic\.?'}
    year = r'( ?(?:19|20)?\d{2}?)?'
    regex = re.compile(r'\b' + day + '(' + mon + '|' + mon_lang.get(lang) + ')' + year + r'\b')
    matches = {}
    match = regex.search(text, 0)
    while (match is not None):
        date = match.group()
        for k, v in mon_sub.items():
            date = re.sub(v, k, date)
        try:
            matches.update({match.group(): datetime.strftime(parser.parse(date, dayfirst=True), '%Y-%m-%d')})
        except ParserError as e:
            pass
        match = regex.search(text, match.span()[1])
    for k, v in matches.items():
        text = re.sub(k, v, text)
    result = anonymize_regex(text, r'\d{4}-\d{2}-\d{2}', by, start_tag, end_tag, count, first, False, keep_regex)
    result.update({'replace_dict': {k: result.get('replace_dict').get(v) for k, v in matches.items()}})
    return result


def anonymize_email(text, by='EMAIL', start_tag='#', end_tag='#', count=True, first=1, keep_regex=False):
    """

    :param text:
    :param by:
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param keep_regex:
    :return:
    """
    regex = re.compile(r'\b[\w\.-]+@[\w\.-]+\b')
    return anonymize_regex(text, regex, by, start_tag, end_tag, count, first, False, keep_regex)


def anonymize_names(text, first_names_regex, last_names_regex, sep=r'[\s,\n]', by='NAME', start_tag='#', end_tag='#',
                    count=True, first=1, keep_regex=False):
    """

    :param text:
    :param first_names_regex:
    :param last_names_regex:
    :param sep:
    :param by:
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param keep_regex:
    :return:
    """
    def _find_names(text, names_regex):
        found_names = re.finditer(names_regex, text, overlapped=True)
        return sorted(list(set(f.group() for f in found_names if len(f.group()) > 0)), key=len, reverse=True)
    
    first_names, last_names = _find_names(text, first_names_regex), _find_names(text, last_names_regex)
    combos = (list(product(first_names, last_names)) + list(product(set(f[0] + r'\.' for f in first_names), last_names))
              + list(product(first_names, set(l[0] + r'\.' for l in last_names))))
    rgx = ([re.compile(r'\b(?:' + f[0] + r')' + sep + r'+(?:' + f[1] 
                      + r')|(?:' + f[1] + r')' + sep + r'+(?:' + f[0] + r')\b') for f in combos])
    rgx = rgx + [re.compile(r'\b(?:' + n + r')\b') for n in sorted(list(set(first_names + last_names)), key=len, reverse=True)] 
    result = {'text': text, 'replace_dict': {}} | ({'regex': [], 'matches': []} if keep_regex else {})
    for r in rgx:
        result = _update_result(result, anonymize_regex(result.get('text'), r, by=by, start_tag=start_tag, end_tag=end_tag, count=count,
                               first=first + len(result.get('replace_dict')), keep_regex=keep_regex))
    return result


def anonymize_percentage(text, by='PERC', start_tag='#', end_tag='#', count=True, first=1, keep_regex=False, decimal_regex=r'\.'):
    """
    :param text:
    :param by:
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param keep_regex
    :param decimal_regex:
    :return:
    """
    regex = r'(?:-?\d+(?:' + decimal_regex + r'\d+)? ?%)'
    return anonymize_regex(text, re.compile(regex), by, start_tag, end_tag, count, first, False, keep_regex)


def anonymize_phone(text, by='PHONE', start_tag='#', end_tag='#', count=True, first=1, keep_regex=False, country_codes=COUNTRY_CODES_REGEX):
    """
    :param text:
    :param by:
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param keep_regex:
    :param country_codes:
    :return:
    """
    regex = re.compile(r'(\b(00(' + country_codes + r')|0)|\B(\+(' + country_codes
                       + r')))(\s?\(0\))?(\s)?[1-9]{2}([\s\/\-])?[0-9]{3}([\s\/\-])?[0-9]{2}([\s\/\-])?[0-9]{2}\b')
    return anonymize_regex(text, regex, by, start_tag, end_tag, count, first, False, keep_regex)


def anonymize_entities(text, by_ahv='AHV', by_phone='PHONE', by_currencies='CURRENCY', by_email='EMAIL', by_dates='DATE', by_names='PERSON',
                       first_names=first_trie_regex, last_names=last_trie_regex, start_tag='#', end_tag='#', count=True, first=1, flip_replace_dict=True, keep_regex=False):
    """
    
    :param text:
    :param by_ahv:
    :param by_phone:
    :param by_currencies:
    :param by_email:
    :param by_dates:
    :param by_names:
    :param first_names: list or precompiled regex
    :param last_names: list or precompiled regex
    :param start_tag:
    :param end_tag:
    :param count:
    :param first:
    :param flip_replace_dict:
    :param keep_regex:
    :return:
    """
    result = {'text': text, 'replace_dict': {}} | ({'regex': [], 'matches': []} if keep_regex else {})
    if by_ahv is not None:
        _update_result(result, anonymize_ahv(result.get('text'), by=by_ahv, start_tag=start_tag, end_tag=end_tag, 
                                            count=count, first=first, keep_regex=keep_regex))
    if by_phone is not None:
        _update_result(result, anonymize_phone(result.get('text'), by=by_phone, start_tag=start_tag, end_tag=end_tag, 
                                              count=count, first=first, keep_regex=keep_regex))
    if by_currencies is not None:
        _update_result(result, anonymize_currency(result.get('text'), by=by_currencies, start_tag=start_tag, end_tag=end_tag, 
                                                 count=count, first=first, keep_regex=keep_regex))
    if by_email is not None:
        _update_result(result, anonymize_email(result.get('text'), by=by_email, start_tag=start_tag, end_tag=end_tag, 
                                              count=count, first=first, keep_regex=keep_regex))
    if by_dates is not None:
        _update_result(result, anonymize_dates(result.get('text'), by=by_dates, start_tag=start_tag, end_tag=end_tag,
                                              count=count, first=first, keep_regex=keep_regex))
    if (by_names is not None) & (first_names is not None) & (last_names is not None):
        first_names_regex = create_names_regex(first_names) 
        last_names_regex = create_names_regex(last_names)
        _update_result(result, anonymize_names(result.get('text'), first_names_regex=first_names_regex, last_names_regex=last_names_regex,
                                              by=by_names, start_tag=start_tag, end_tag=end_tag, count=count, first=first,
                                              keep_regex=keep_regex))
    if flip_replace_dict:
        result['replace_dict'] = _flip_replace_dict(result.get('replace_dict'))
    return result


def demo():
    print('Email')
    text = 'My email is tom@example.com and yours is jerry@example.com. Yes it is jerry@example.com'
    for k, v in ({'original': text} | anonymize_email(text)).items():
        print(f'{k}: {v}')
    print('\n')

    print('Währung')
    text = "Wir haben heute CHF 15'000 ausgegeben, das ist mehr als die 10 000 Franken die wir geplant hatten"
    for k, v in ({'original': text} | anonymize_currency(text)).items():
        print(f'{k}: {v}')
    print('\n')

    print('Telefonnummer')
    text = 'Meine Nummer ist 076-123-45-67 und nicht etwa 076 123 4568. Mit Country Code wär sie 0041 76 123 45 67 oder +41 (0)76 1234567'
    for k, v in ({'original': text} | anonymize_phone(text)).items():
        print(f'{k}: {v}')
    print('\n')

    print('Vorgegebener Name Max Mustermann')
    text = 'Mein Name ist Max Mustermann bzw. Mustermann, Max, abgekürzt auch M. Mustermann oder Mr. Mustermann'
    for k, v in ({'original': text} | anonymize_names(text, re.compile('Max'), re.compile('Mustermann'))).items():
        print(f'{k}: {v}')
    print('\n')

    print('Datumswerte')
    text = 'Der 4. Januar 2025, der 4.1.25 und der 5.7.2023 sind Datumswerte.'
    for k, v in ({'original': text} | anonymize_dates(text)).items():
        print(f'{k}: {v}')
        