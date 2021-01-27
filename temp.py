# import module
from bs4 import BeautifulSoup

# URL for scrapping data
markup = '<div style="display:inline" class="fn org country-name">\
Democratic Republic of<br /> São Tomé and Príncipe <i>unwanted thing</i></div>'

# get URL html
lftData = BeautifulSoup(markup, 'lxml')

print(lftData)
# <div style="display:inline" class="fn org country-name">Democratic Republic of <br />São Tomé and Príncipe <i>unwanted thing</i></div>

for br_tag in lftData("br"):
    lftData.br.unwrap()

print(lftData)

# <div style="display:inline" class="fn org country-name">Democratic Republic of São Tomé and Príncipe <i>unwanted thing</i></div>

country_name = BeautifulSoup(str(lftData), 'lxml').get_text(
    separator=", ", strip=True).split(', ')[0]

print(country_name)

# Democratic Republic of

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
