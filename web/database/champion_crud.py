from os import getenv
from dotenv import load_dotenv
from time import time
import pyrebase


load_dotenv('E:\\Dev\\Python\\Bot\\discord-bot-py\\.env')

class Champion:
	def __init__(self, name, winrate):
		self._name = name
		self._data = {'winrate': winrate}

class ChampionDAO:
	CONFIGS = {
		'apiKey': 				getenv('FIREBASE_API_KEY'),
		'authDomain': 			getenv('FIREBASE_AUTH_DOMAIN'),
		'databaseURL': 			getenv('FIREBASE_DATABASE_URL'),
		'projectId': 			getenv('FIREBASE_PROJECT_ID'),
		'storageBucket': 		getenv('FIREBASE_STORAGE_BUCKET'),
		'messagingSenderId': 	getenv('FIREBASE_MESSAGING_SENDER_ID'),
		'appId': 				getenv('FIREBASE_APP_ID')
	}	

	def __init__(self):
		self.firebase = pyrebase.initialize_app(ChampionDAO.CONFIGS)
		self.database = self.firebase.database()
		self.table = 'Champions'

	def save(self, champion):
		self.database.child(self.table).set({'created_at': time()})
		self.database.child(self.table).child(champion._name).set(champion._data)

	def fetch(self, champion_name):
		return self.database.child(self.table).child(champion_name).get().val()
	
	def fetch_all(self):
		return self.database.child(self.table).get().val()
