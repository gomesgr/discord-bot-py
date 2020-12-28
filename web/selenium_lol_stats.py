import re
from collections import OrderedDict
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import selenium_lol_live_game

URL = 'https://br.op.gg/statistics/champion/'

FIND = '//*[@id="ChampionStatsTable"]'
FIND2 = '//*[@role="row"]'

options = webdriver.ChromeOptions()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--headless")

exp = '[A-Za-z]+'

def fill_dict() -> dict:
	ls = {}
	with webdriver.Chrome(options=options,
		executable_path='E:\\Dev\\Python\\Selenium\\chromedriver.exe') as driver:
		driver.get(URL)

		html = driver.find_element_by_tag_name('html')
		html.send_keys(Keys.END)	

		page = driver.page_source
		res = driver.find_elements_by_xpath(FIND2)
		for element in res:
			splitted = element.text.split()
			
			if re.search(exp, splitted[3]):
				name = remove_quote(splitted[1].lower() + splitted[2].lower() + splitted[3].lower())
				wr = splitted[4]
			elif re.search(exp, splitted[2]):
				name = remove_quote(splitted[1].lower() + splitted[2].lower())
				wr = splitted[3]
			else:
				name = remove_quote(splitted[1].lower())
				wr = splitted[2]
			# print(f'{name}: {wr}')
			ls[name] = wr
	return ls
	
def remove_quote(word):
	if '\'' in word:
		return word.replace('\'', '')
	if '.' in word:
		return word.replace('.', '')
	return word


def fill_winrates(stats, username) -> dict:
	wrs = {}
	for champion in selenium_lol_live_game.get_live_champions(username):
		wrs[champion] = (stats.get(champion))
	return get_winrates(wrs)

calc_winrate = lambda i: float(i.split('%')[0]) / 100 

def get_winrates(winrate_per_champ):
	wr_red = []
	wr_blue = []
	i=0
	for winrate in winrate_per_champ.values():
		if i > 4:
			wr_red.append(winrate)
		else:
			wr_blue.append(winrate)
		i += 1
	red = sum(list(map(calc_winrate, wr_red))) / 5 * 100
	blu = sum(list(map(calc_winrate, wr_blue))) / 5 * 100
	return f'{red:.1f}', f'{blu:.1f}'



if __name__ == '__main__':
	stats = fill_dict()
	winrates = fill_winrates(stats)
	print(stats)


'''
porcentagens = [0.52, 0.49, 0.45, 0.51, 0.42]
porcentagens2 = [0.53, 0.54, 0.50, 0.49, 0.48]
print(f'{sum(porcentagens) / 5 * 100:.1f}%')
print(f'{sum(porcentagens2) / 5 * 100:.1f}%')
'''
