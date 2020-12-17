# Constants
LEAGUE_OPGG 		= '-opgg'
PING 				= '-ping'
PREFIX				= '$kt'

# Currency
DOLAR				= '-dolar'
EURO 				= '-euro'
LIBRA 				= '-libra'
DOLAR_AUSTRALIANO	= '-dolara'
DOLAR_CANADENSE		= '-dolarc'

CURRENCIES = {
			DOLAR: 0,
			EURO: 1,
			LIBRA: 2,
			DOLAR_AUSTRALIANO: 3,
			DOLAR_CANADENSE: 4
		}

class Commands:
	
	def fetch_league_name(self, command):
		return command.replace(LEAGUE_OPGG, '')

	def separate(self, command):
		return command.split(' ')[1:]

	def current_coin(currency):
		pass