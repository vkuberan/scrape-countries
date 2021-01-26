# A small scraper used to scrape 'member countries of united nations'
# from wikipedia and saves important informations like president,
# population, gdp, etc., in a json file.
# Wiki: 'https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations'

from helper import *
import os
import glob
import time
import json


project_dirs = {
    'src': 'wiki',
    'html_dir': 'wiki/html',
    'data_dir': 'wiki/data'
}

link_data = {}

create_related_dirs(project_dirs)

msg = '''Do you want to fetch fresh data from the wiki?
Y for yes and any key for No..."
'''
fetch_new_data = (input(msg).strip().upper() or 'N')[0]

if fetch_new_data == 'Y':
    for key, value in project_dirs.items():
        del_dir = ''
        if key == 'src':
            pass
        elif key == 'html_dir':
            del_dir = value + '/*.html'
        elif key == 'data_dir':
            del_dir = value + '/*.json'

        if del_dir != '':
            files = glob.glob(del_dir)
            for f in files:
                os.remove(f)

clear_screen()

wiki_countries_source = 'https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations'

msg = "Extracting countries list from Wikipedia Source: {}".format(
    wiki_countries_source)

print_char_under_string(msg, '-')

html_file_to_save = '/'.join([project_dirs['html_dir'], 'all-countries.html'])

# fetch data from the source
data = fetch_data(wiki_countries_source, html_file_to_save)

json_file_to_save = '/'.join([project_dirs['data_dir'], 'all-countries.json'])

# parse the data to get list of all countries
list_of_all_countries = get_list_of_all_countries(
    'wiki', data, json_file_to_save)

iCnt = 1
for country, values in list_of_all_countries.items():
    date_joined = values[2]
    link_source = '/'.join(['https://en.wikipedia.org', values[1]])
    html_file_to_save = '/'.join([project_dirs['html_dir'], values[3]])
    data_file = values[4]

    msg = "{:<3}: '{}' Joined on {}, Wiki Source: {}".format(
        iCnt, country, date_joined, link_source)

    print_char_under_string(msg, '-', '\n\n')

    # fetch data from wiki source
    data = fetch_data(link_source, html_file_to_save)

    country_details = get_country_details(
        project_dirs, 'wiki', data, data_file)

    time.sleep(1)

    # if iCnt >= 180:
    #     input("Press any key to continue...")

    iCnt += 1
    clear_screen()
