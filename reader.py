import json
import string
from tqdm import tqdm

def read(filename, n_articles=None):
    with open(filename, 'r', encoding='utf-8') as file:
        json_object = ''
        reading = False
        n = 0
        for line in file:
            json_object += line
            if line[0] == '}':
                d = json.loads(json_object.strip()[:-1])
                n += 1
                yield d
                if n_articles is not None and n >= n_articles:
                    break
                json_object = ''

def clean(body):
    return ' '.join(
        body.translate(
            str.maketrans(
                string.punctuation, ' '*len(string.punctuation)
            )
        ).split()
    )

if __name__ == '__main__':
    reader = read('habr.json')
    count = 0
    count_big = 0

    a = next(reader)

    print('example of cleaning: \n\t%s...\n' % clean(a['main_body'])[:2000])

    for a in tqdm(reader):
        if len(clean(a['main_body'])) >= 2000:
            count_big += 1
        count += 1

    print("N of articles: %d\nN of articles bigger than 2k characters: %d\n" % (count, count_big))