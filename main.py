from bs4 import BeautifulSoup
import requests
import csv
import json


def write_post_to_file(post, file):
    json.dump(post, file, ensure_ascii=False)
    file.write(', ')


def scrape_post_content(post_link):
    post_site = requests.get(post_link).text
    post_site = BeautifulSoup(post_site, 'lxml')

    posts = post_site.find('ol', class_="posts").find_all('li')
    if len(posts) > 0:
        post_content = posts[0].find('blockquote', class_='postcontent').text
        # Format text
        post_content = post_content.replace('\r', '').replace('\n', '').replace('\t', '')
        return post_content
    return ''


def get_post_data(post):
    post_data = {'source': MAIN_LINK}

    title_tag = post.find('a', 'title')
    post_data['link'] = title_tag.attrs['href']
    post_data['title'] = title_tag.text

    author_div = post.find('div', class_='author')
    user_tag = author_div.find('a', 'username')
    post_data['author'] = user_tag.text

    date_label = author_div.find('span')
    # format: [',', date, time]
    post_date = date_label.contents[-1].split('\xa0')
    # Removing ',' element from date
    del post_date[0]

    post_data['date'] = post_date[0]

    thread_stats = post.find('ul', 'threadstats').find_all('li')
    # [# of answers, # of visits, hidden rating(does not work)]
    answers_count = thread_stats[0].find('a')

    # If post is 'Przeniesiony' fields are &nbsp;
    if answers_count is None:
        return post_data

    post_data['answers'] = int(answers_count.text)
    post_data['visits'] = int(thread_stats[1].text.replace('Odwiedzin: ', '').replace(',', ''))

    last_answer_container = post.find("dl", class_='threadlastpost').find_all('dd')
    post_data['last_answer_author'] = last_answer_container[0].find('a', class_='username').find('strong').text
    post_data['last_answer_date'] = last_answer_container[1].contents[0].replace(', ', '')

    post_data['content'] = scrape_post_content(post_data['link'])

    return post_data


def get_all_posts(soup, file):
    threads = soup.findAll('li', class_='threadbit')
    for t in threads:
        write_post_to_file(get_post_data(t), file)


MAIN_LINK = "http://medyczka.pl/forum-ogolne/"

# Connecting to main forum
main_site = requests.get(MAIN_LINK).text
main_soup = BeautifulSoup(main_site, 'lxml')

# Getting page numbers
last_link = main_soup.find('span', attrs={"class": "first_last"}).find('a')
last_index = int(last_link.attrs['href'].strip('http://medyczka.pl/forum-ogolne/'))

# Save all posts into a file
with open("medyczka.json", "w", encoding="utf-8") as fw:
    fw.write('[')
    # Getting posts from first page
    get_all_posts(main_soup, fw)

    # Getting posts from other pages
    for i in range(2, last_index):
        current_site = requests.get(f"{MAIN_LINK}{i}").text
        current_soup = BeautifulSoup(current_site, 'lxml')
        get_all_posts(current_soup, fw)
    # Remove ', ' and close json array
    fw.seek(fw.tell() - 2)
    fw.truncate()
    fw.write(']')
