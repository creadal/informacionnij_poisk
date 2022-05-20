import requests
import bs4
from datetime import datetime
import json

num_articles = 100000

base_url = 'https://habr.com/ru/post/'

starting_index = 0

import time
import random

index = starting_index
posts = 0
while posts < num_articles:
  try:
    time.sleep(random.random() / 5)

    response = requests.get(url=base_url+str(index))
    post = {}
    if response.status_code == 200:
        print(base_url+str(index))
        soup = bs4.BeautifulSoup(response.text)

        post['id'] = index

        post['username'] = soup.find_all('a', {'class': 'tm-user-info__username'})[0].contents[0].strip()
        # post['publish_time'] = datetime.strptime(soup.find_all('time')[0]['title'], '%Y-%m-%d, %H:%M')
        post['publish_time'] = soup.find_all('time')[0]['title']

        if soup.find('h1') is None:
          index -= 1
          continue
        post['title'] = soup.find('h1').find('span').contents[0].strip()

        hubs = []
        for span in soup.find('div', {'class': 'tm-article-snippet__hubs'}).find_all('span'):
          hub = span.find('span')
          if hub is not None:
            hubs.append(hub.contents[0].strip())

        post['hubs'] = hubs

        labels = []
        label_tag = soup.find('div', {'class': 'tm-article-snippet__labels'})
        if label_tag is not None:
          for label in label_tag.find_all('span'):
            labels.append(label.contents[0].strip())

        post['labels'] = labels

        main_body = ''
        for tag in soup.find('div', {'class': 'tm-article-body'}).find_all():
          if len(main_body) > 0 and main_body[-1] != '\n':
            main_body += '\n'
          main_body += tag.text

        post['main_body'] = main_body

        figures = []
        for figure in soup.find('div', {'class': 'tm-article-body'}).find_all('figure'):
          figures.append({'src': figure.find('img')['src'], 'title': figure.find('figcaption').text})

        post['figures'] = figures

        tags = []
        for tag in soup.find_all('span', string='Теги:')[0].fetchParents()[0].find_all('a'):
          tags.append(tag.contents[0])

        post['tags'] = tags

        post['rating'] = int(soup.select('span[class^=tm-votes-meter]')[0].text)

        posts += 1

        print('%d/%d\n' % (posts, num_articles))

        with open('habr2.json', 'ab') as json_file:
          json_file.write(json.dumps(post, indent=4, ensure_ascii=False).encode('utf-8') + bytes(',\n', encoding='utf-8'))
  except Exception as e:
      print(e)
  finally:
      index += 1
      continue

