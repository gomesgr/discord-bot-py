from urllib.request import urlopen
from typing import List
from bs4 import BeautifulSoup


def find_rank(nickname: List[str]) -> str:
    nickname = '%20'.join(nickname)
    ugg_url = f'https://u.gg/lol/profile/br1/{nickname}'
    ranks = {
        'Iron': 'Ferro',
        'Bronze': 'Bronze',
        'Silver': 'Prata',
        'Gold': 'Ouro',
        'Platinum': 'Platina',
        'Diamond': 'Diamante',
        'Master': 'Mestre',
        'Grandmaster': 'Grão-Mestre',
        'Challenger': 'Desafiante'}

    bs = BeautifulSoup(urlopen(ugg_url).read(), 'lxml')
    full_content = bs.title(string=True)[0]
    spl = full_content.split(' ')

    rank = []

    for x in spl:
        if x in ranks.keys():
            print(ranks.get(x))
            rank.append(ranks.get(x))
        if x.isnumeric():
            rank.append(x)
            break
    return ' '.join(rank)


if __name__ == '__main__':
    pass
