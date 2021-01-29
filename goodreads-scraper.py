from helper import *
import os
import glob
import time
import json
import re

project_dirs = {
    'src': 'wiki',
    'html_dir': 'goodreads/html',
    'data_dir': 'goodreads/data'
}

link_data = {}

create_related_dirs(project_dirs)

# msg = '''Do you want to fetch fresh data from the Goodreads?
# Y for yes and any key for No..."
# '''
# fetch_new_data = (input(msg).strip().upper() or 'N')[0]

# if fetch_new_data == 'Y':
#     for key, value in project_dirs.items():
#         del_dir = ''
#         if key == 'src':
#             pass
#         elif key == 'html_dir':
#             del_dir = value + '/*.html'
#         elif key == 'data_dir':
#             del_dir = value + '/*.json'

#         if del_dir != '':
#             files = glob.glob(del_dir)
#             for f in files:
#                 os.remove(f)

# clear_screen()


authors = {
    'pushkin': 'https://www.goodreads.com/author/show/16070.Alexander_Pushkin',
    'leo-tolstoy': 'https://www.goodreads.com/author/show/128382.Leo_Tolstoy',
    'fyodor-dostoyevsky': 'https://www.goodreads.com/author/show/3137322.Fyodor_Dostoyevsky',
    'jrr-tolkein': 'https://www.goodreads.com/author/show/656983.J_R_R_Tolkien',
    'paulo-coelho': 'https://www.goodreads.com/author/show/566.Paulo_Coelho'
}

for author_name, url in authors.items():
    html_to_save = '/'.join([project_dirs['html_dir'], author_name + '.html'])

    msg = "Extracting {} from Goodreads.com: {}".format(
        author_name, html_to_save)

    print_char_under_string(msg, '-')

    data = fetch_data(url, html_to_save)

    soup = BeautifulSoup(data, 'lxml')

    author_full_name = soup.find(
        'h1', class_='authorName').get_text(strip=True)

    # contains usefull informations about the author
    data_title = soup.find_all('div', class_='dataTitle')
    data_item = soup.find_all('div', class_='dataItem')

    iCnt = 0
    author_details = {}
    for dt in data_title:

        key = dt.get_text(strip=True)
        value = ''
        # special case because text found without a tag
        if iCnt == 0:
            value = dt.nextSibling

        value += data_item[iCnt].get_text(strip=True)

        author_details[key] = value

        iCnt += 1

    author_bio = soup.find(
        'div', class_='aboutAuthorInfo').get_text(strip=True)
    author_details['bio'] = author_bio

    author_details['avg_rating'] = soup.find(
        'span', itemprop='ratingValue').get_text(strip=True)
    author_details['rating_count'] = soup.find(
        'span', itemprop='ratingCount').get_text(strip=True)
    author_details['review_count'] = soup.find(
        'span', itemprop='reviewCount').get_text(strip=True)

    # get top 10 books of this author
    top_books = soup.find('table', class_='tableList').find_all('tr')

    top_books_list = {}

    iCnt = 1
    for book in top_books:
        details = book.find_all('td')
        book_cover = details[0].find('img').get('src')
        book_title = details[1].find(
            'a', class_='bookTitle').get_text(strip=True)
        book_rating = details[1].find(
            'span', class_='minirating').get_text(strip=True)
        book_rating = re.sub(r'(\\r|\\n)+', '', book_rating).strip()
        book_published = details[1].find(
            'span', class_='minirating').nextSibling
        book_published = re.sub(
            '(\\r|\\n| )', ' ', book_published).replace('—', '').strip()
        book_published = re.sub(
            ' +', ' ', book_published).replace('published', 'published in')

        # print(details[1])
        top_books_list[iCnt] = {
            'Cover Image': book_cover,
            'Title': book_title,
            'Rating': book_rating,
            'Published': book_published,
        }
        iCnt += 1

    print("Author Full Name: ", author_full_name)
    print(author_details)
    print(top_books_list)

    input("Press any key to continue")
    clear_screen()


# html_file_to_save = '/'.join([project_dirs['html_dir'], 'all-countries.html'])
