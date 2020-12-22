from time import sleep

from selenium import webdriver
from selenium.common.exceptions import (NoAlertPresentException, NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from discord import Colour

# USER = 'splex'
URL = 'https://br.op.gg/summoner/userName=?'
UPDATE_SUMMON_BUTTON = '//*[@id="SummonerRefreshButton"]'
TIER_SOLO = '//*[@class="TierRank"]'
TIER_FLEX = '//*[@class="sub-tier__rank-tier "]'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--data-reduction-proxy-client-config')

class LookForRank:
	def __init__(self, user):
		self.user = user
		self.url = URL.replace('?', user)
		self.names = {
			'Iron': ('Ferro', Colour.light_gray()),
			'Bronze': ('Bronze', Colour.blurple()),
			'Silver': ('Prata', Colour.darker_gray()), 
			'Gold': ('Ouro', Colour.gold()), 
			'Platinum': ('Platina', Colour.teal()), 
			'Diamond': ('Diamante', Colour.blue()),
			'Master': ('Mestre', Colour.dark_purple())
		}

	def init(self):
		with webdriver.Chrome(options=chrome_options,
			executable_path='E:\\Dev\\Python\\Selenium\\chromedriver.exe') as driver:
			try:
				driver.get(self.url)
				
				refresh_summoner_button = driver.find_element_by_xpath(UPDATE_SUMMON_BUTTON)
				refresh_summoner_button.click()
				sleep(.5)
				alert = driver.switch_to.alert
				alert.accept()
			except NoAlertPresentException:
				print('Alert found!')
			finally:
				return self.find_rank(driver)

	def find_rank(self, driver):
		try:
			tier_s = driver.find_element_by_xpath(TIER_SOLO)
			rank_name = tier_s.text.split()[0]
			if len(tier_s.text.split()) < 2:
				return self.names[rank_name][0]
			rank_number = tier_s.text.split()[1]
			var =  self.names[rank_name][0] + ' ' + rank_number
			return var
		except NoSuchElementException:
			try:
				tier_f = driver.find_element_by_xpath(TIER_FLEX)
				rank_name = tier_f.text.split()[0]
				if len(tier_f.text.split()) < 2:
					return self.names[rank_name][0]
				rank_number = tier_f.text.split()[1]
				return self.names[rank_name][0] + ' ' + rank_number
			except NoSuchElementException:
				return 'Sem elo'	

if __name__ == '__main__':
	x = init('themrhetch')
