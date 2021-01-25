def wiki_parse_capital_city(lftData, city_info):
    ret_capital = ''
    ret_largest = ''
    clean_city_info = []

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

    print(clean_city_info)
    if len(clean_city_info) == 1:
        capital_city = clean_city_info[0]
    elif len(clean_city_info) >= 3:
        capital_city = clean_city_info[0]
        lat = clean_city_info[1]
        lon = clean_city_info[2]

    ret_capital = [capital_city, {
        'lat': lat, 'lon': lon}]

    if 'largest city' in lftData:
        ret_largest = [capital_city, {
            'lat': lat, 'lon': lon}]

    return ret_capital, ret_largest
