import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


options = webdriver.ChromeOptions()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--headless")

LIVE_GAME = '//*[@class="SpectateTabButton SpectateTabButtonActive"]'
FIND = '//*[@class="ChampionImage Cell"]/a'

def get_live_champions(username):
	URL = 'https://br.op.gg/summoner/userName={}'
	URL = URL.format(username)
	try:
		champions = []
		with webdriver.Chrome(options=options, 
			executable_path='E:\\Dev\\Python\\Selenium\\chromedriver.exe') as driver:
			driver.get(URL)
			
			pattern = re.compile('champion/{1}[A-Za-z]+')

			live_btn = driver.find_element_by_xpath(LIVE_GAME)
			live_btn.click()

			sleep(2)

			html = driver.find_element_by_tag_name('html')
			html.send_keys(Keys.END)
			res = driver.find_elements_by_xpath(FIND)
			for element in res:
				champions.append(pattern.findall(element.get_property('href'))[0].split('/')[1])
		return champions
	except NoSuchElementException:
		return None
			
if __name__=='__main__':
	print(get_live_champions())
