import pyrebase
from os import getenv
from dotenv import load_dotenv
from time import (sleep, time)

load_dotenv('E:\\Dev\\Python\\Bot\\discord-bot-py\\.env')

class Player:
	def __init__(self, username, rank,  created_at=time()):
		self._username = username
		self._data = {
			'rank': rank,
			'created_at': created_at
		}

	def __str__(self):
		return f'''
username: {self._username},
rank: {self._data['rank']},
criado_em: {self._data['created_at']}'''

class PlayerDAO:
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
		self.firebase = pyrebase.initialize_app(PlayerDAO.CONFIGS)
		self.database = self.firebase.database()
		self.table = 'Players'

	def save(self, player):
		self.database.child(self.table).child(player._username).set(player._data)

	def fetch(self, username):
		return self.database.child(self.table).child(username).get().val()


if __name__ == '__main__':
	pdao = PlayerDAO()
	print(pdao.fetch('themrhetch'))

	data = {
		'rank': 'platina 3',
		'created_at': time()
	}

	# database.child('Players').child('themrhetch').set(data)