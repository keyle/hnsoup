from bs4 import BeautifulSoup
import requests
import sys
import time

seen = {}


def pull_feed():
    global seen
    url = requests.get('https://hnrss.org/newcomments')

    soup = BeautifulSoup(url.content, 'xml')
    entries = soup.find_all('item')

    for i in entries:
        desc = BeautifulSoup(i.description.text, 'lxml').text
        if desc in seen:
            continue

        seen[desc] = 1

        title = i.title.text
        link = i.guid.text
        blob = f'\033[31m{title}\n\033[93m{desc}\033[30m\n{link}\033[0m\n'

        for line in blob.splitlines():
            for w in line.split():
                sys.stdout.write("%s " % w)
                sys.stdout.flush()
                time.sleep(0.03)
            print('')
        print('')

        time.sleep(2)

    # print('\033[30m__EOS__')
    time.sleep(33)


try:
    while True:
        pull_feed()
except KeyboardInterrupt:
    print('\033[0m \ninterrupted!')
