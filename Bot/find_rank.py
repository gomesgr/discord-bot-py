import requests
from bs4 import BeautifulSoup


def find_rank(nickname):
    nickname = '%20'.join(nickname.split(' '))
    link = f'https://u.gg/lol/profile/br1/{nickname}'
    ranks = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster', 'Challenger']
    bs = BeautifulSoup(requests.get(link).text, 'html.parser')
    full_content = bs.title(string=True)[0]
    spl = full_content.split(' ')

    rank = []

    for x in spl:
        if x in ranks:
            rank.append(x)
        if x.isnumeric():
            rank.append(x)
            break
    return ' '.join(rank)


if __name__ == '__main__':
    pass
