from bs4 import BeautifulSoup
import requests
import sys
import time
import argparse

parser = argparse.ArgumentParser(description='HN for your face in terminal.')
parser.add_argument('--type', type=str, default='comments', help='type of content `posts` or `comments` (default)')

args = parser.parse_args()

seen = {}

comments = args.type == 'comments'

def pull_feed():
    global seen
    url = requests.get('https://hnrss.org/newcomments' if comments else 'https://hnrss.org/newest')

    soup = BeautifulSoup(url.content, 'xml')
    entries = soup.find_all('item')

    for i in entries:
        title = i.title.text
        desc = BeautifulSoup(i.description.text, 'lxml').text

        if title in seen or desc in seen:
            continue
        if args.type == 'comments':
            seen[desc] = 1
        else:
            seen[title] = 1

        link = i.guid.text
        blob = f'\n\033[31m{title}\n\033[93m{desc}\033[30m\n{link}\033[0m'

        for line in blob.splitlines():
            for w in line.split():
                sys.stdout.write("%s " % w)
                sys.stdout.flush()
                time.sleep(0.03)
            print('')

        time.sleep(2)

    sys.stdout.write('\033[30m~ ')
    sys.stdout.flush()
    time.sleep(35 if comments else 60)


try:
    while True:
        pull_feed()
except KeyboardInterrupt:
    print('\033[0m \ninterrupted!')
