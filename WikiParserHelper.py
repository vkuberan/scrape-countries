import re
from bs4 import BeautifulSoup


def wiki_replace_unicode(wiki_string, list_of_replacements):
    for key, val in list_of_replacements.items():
        wiki_string = wiki_string.replace(key, val)

    return wiki_string


def wiki_parse_country(lftData):

    lftData = lftData.find("div", class_='country-name')

    for br_tag in lftData("br"):
        lftData.br.unwrap()

    lftData = BeautifulSoup(str(lftData), 'lxml')

    country_name = lftData.get_text(separator=", ", strip=True)

    # some filter conditions
    # São Tomé and Príncipe
    if "ofS" in country_name:
        country_name = country_name.replace("ofS", "of S")
    elif "Sri Lanka" in country_name:
        country_name = country_name.replace(",", "")
    else:
        country_name = country_name.split(",")[0]

    return country_name


def wiki_parse_capital_city(lftData, city_info):
    ret_capital = ''
    ret_largest = ''
    clean_city_info = []

    # replacble chars
    lp = {
        u'\u00b0': ' Deg ',
        u'\u2032': ' Min ',
        u'\u2033': ' Sec ',
    }

    if city_info != '':

        # another way to remove empty elements from the list
        # city_info = list(
        #     filter(None, list(
        #         [x.strip() for x in city_info.split(',') if x != ''])))

        city_info = [x.strip() for x in city_info.split(',')]
        city_info = [x for x in city_info if x != '']
        clean_city_info = [x for x in city_info[1:] if x[0].isdigit()]
        clean_city_info.insert(0, city_info[0])

    capital_city = ''
    lat = ''
    lon = ''

    if len(clean_city_info) == 1:
        capital_city = clean_city_info[0]
    elif len(clean_city_info) >= 3:
        capital_city = clean_city_info[0]
        # lat = (clean_city_info[1].encode('ascii', 'ignore')).decode('utf-8')
        # lon = (clean_city_info[2].encode('ascii', 'ignore')).decode('utf-8')
        lat = wiki_replace_unicode(clean_city_info[1], lp)
        lon = wiki_replace_unicode(clean_city_info[2], lp)

    ret_capital = [capital_city, {
        'latitude': lat, 'longitude': lon}]

    if 'largest city' in lftData:
        ret_largest = capital_city

    return ret_capital, ret_largest


def wiki_clean_left_side(lft):
    # replacble chars
    lp = {
        '•': ''
    }

    is_child = 0  # 0 if parent, 1 is child

    if '•' in lft:
        is_child = 1
        lft = wiki_replace_unicode(lft, lp).split(',')
        if len(lft) >= 2:
            lft = ' '.join(lft[1:])
        else:
            lft = lft[0]

    lft = wiki_replace_unicode(lft, {'\u00a0': ' '}).strip()

    return lft, is_child


def wiki_clean_right_side(rgt):
    lp = {
        '\u00a0': ' ',
        '\u00b7': ' '
    }

    rgt = wiki_replace_unicode(rgt, lp).strip()
    rgt = re.sub(r'\[.*\]', '', rgt)
    return rgt
