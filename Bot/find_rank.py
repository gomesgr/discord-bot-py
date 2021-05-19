import requests
from bs4 import BeautifulSoup


def find_rank(nickname):
	nickname = '%20'.join(nickname.split(' '))
	link = f'https://u.gg/lol/profile/br1/{nickname}'
	ranks = {'Iron': 'Ferro', 'Bronze': 'Bronze', 'Silver': 'Prata', 'Gold': 'Ouro', 'Platinum': 'Platina',
	         'Diamond': 'Diamante', 'Master': 'Mestre', 'Grandmaster': 'Grão-Mestre', 'Challenger': 'Desafiante'}

	bs = BeautifulSoup(requests.get(link).text, 'html.parser')
	full_content = bs.title(string=True)[0]
	print(full_content)
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
