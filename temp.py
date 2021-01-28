languages = '•, Pashto, [1], •, Dari Persian'.split(',')
languages = [x.strip()
             for x in languages if all(y.isalpha() or y.isspace() for y in x)]
print(languages)

exit()
# lftData = BeautifulSoup(str(lftData), 'lxml')


def wiki_replace_unicode(wiki_string, list_of_replacements):
    for key, val in list_of_replacements.items():
        wiki_string = wiki_string.replace(key, val)

    return wiki_string


special = u"\u2022"
abc = u'ABC•def'
print(abc)
abc = abc.replace(special, 'X')
print(abc)

lp = {
    u'\u00b0': ' Dec ',
    u'\u2032': ' M '
}

degrees = ' Degrees '
degrees_spe = u'\u00b0'

minutes = ' Minutes '
minutes_spe = u'\u2032'

albania_lat = '41°19′N'
albania_lon = '19°49′E'

albania_lat = wiki_replace_unicode(albania_lat, lp)
print(albania_lat)
