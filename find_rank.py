from typing import List, Optional
from urllib.request import urlopen

from bs4 import BeautifulSoup


def find_rank(nickname_list: List[str]) -> str:
    nickname: str = '%20'.join(nickname_list)
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
    spl: List[str] = full_content.split(' ')

    rank: List[str] = []

    for x in spl:
        if x in ranks.keys():
            print(ranks.get(x))
            rank.append(str(ranks.get(x)))
        if x.isnumeric():
            rank.append(x)
            break
    return ' '.join(rank)


if __name__ == '__main__':
    pass
