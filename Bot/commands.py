# Constants
LEAGUE_OPGG = '-opgg'
PING = '-ping'

class Commands:
	def __init__(self):
		self.prefix = '$kt'
	
	def fetch_league_name(self, command):
		return command.replace(LEAGUE_OPGG, '')

	def separate(self, command):
		return command.split(' ')