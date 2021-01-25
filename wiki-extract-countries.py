from common import *
import json
from bs4 import BeautifulSoup
import requests


project_dirs = {
    'src': 'wiki',
    'html_dir': 'wiki/html',
    'data_dir': 'wiki/data'
}

create_related_dirs(project_dirs)

wiki_countries_entry = {
    'India': ['https://en.wikipedia.org/wiki/India', 'india.html', 'india.json'],
    'United States': ['https://en.wikipedia.org/wiki/United_States', 'us.html', 'us.json'],
    'China': ['https://en.wikipedia.org/wiki/China', ' china.html', 'china.json'],
    'United Kingdom': ['https://en.wikipedia.org/wiki/United_Kingdom', 'uk.html', 'uk.json'],
    'France': ['https://en.wikipedia.org/wiki/France', 'france.html', 'france.json'],
    'Germany': ['https://en.wikipedia.org/wiki/Germany', 'germany.html', 'germany.json'],
}

for country, properties in wiki_countries_entry.items():

    country_data = {}

    clear_screen()
    commonStr = "Extracting {}'s general information from Wikipedia".format(
        country)
    print_char_under_string(commonStr)

    link_source = properties[0]
    html_file = '/'.join([project_dirs['html_dir'], properties[1]])
    data_file = '/'.join([project_dirs['data_dir'], properties[2]])

    commonStr = "Wikipedia Link: {}, Files: [HTML: {}, Data: {}]".format(
        link_source, html_file, data_file)
    print_char_under_string(commonStr, '-')

    try:
        with open(html_file, 'rb') as hs:
            html_source = hs.read().decode("UTF-8")
            print_char_under_string(
                "Fetching info from the crawled file.", '-', '\n')
            soup = BeautifulSoup(html_source, 'lxml')
            # print(soup.prettify())
    except:
        print_char_under_string(
            "Fetching data from the server using request.", '-', '\n')
        res = requests.get(link_source)
        soup = BeautifulSoup(res.text, 'lxml')
        f = open(html_file, mode='w', encoding='UTF-8')
        f.write(res.text)
        f.close()

    details = soup.find('table', class_='infobox geography vcard').find(
        "tbody").find_all("tr")

    prev = ''
    for detail in details:
        # we are going to get the details
        lftData = detail.find("th")
        rgtData = detail.find("td")

        if (lftData != None and rgtData != None):
            lftData = detail.find("th").get_text()
            rgtData = detail.find("td").get_text(separator=', ', strip=True)
            print(lftData, rgtData)

        else:
            if lftData:
                if lftData.find("div", class_='country-name'):
                    # to get the entire text separated by commna (or any char) of an element
                    # data = lftData.get_text(
                    #     separator=", ", strip=True)
                    country_data['country-name'] = lftData.find(
                        "div", class_='country-name').get_text()
                # else:
                #     data = lftData.get_text(
                #         separator=", ", strip=True)
                #     print(data)

    print(country_data)
    input("\nPress any key to continue...")
    clear_screen()
