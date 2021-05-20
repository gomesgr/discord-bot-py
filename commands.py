# Constants
LEAGUE_OPGG = 'lol'
PING = 'ping'
TEST = 't'
COMMANDS = 'c'
PERDEMO = 'perdemo'
DISTORCER = 'distorcer'
# Prefixo
PREFIX = 'k'

# Currency
DOLAR = 'dolar'
EURO = 'euro'
LIBRA = 'libra'
DOLAR_AUSTRALIANO = 'dolara'
DOLAR_CANADENSE = 'dolarc'

# Crypto
CRYPTO = 'cry'

CURRENCIES = {
	DOLAR: 0,
	EURO: 1,
	LIBRA: 2,
	DOLAR_AUSTRALIANO: 3,
	DOLAR_CANADENSE: 4
}

DIC_CMD = {
	PREFIX: 'Prefixo do Bot',
	PING: 'Retorna um número aleatório',
	LEAGUE_OPGG + ' [username]': 'Retorna o ranque de um usuario no LoL',
	CRYPTO: 'Retorna as cinco mais bem posicionadas criptomoedas',
	DOLAR: 'Retorna o valor do dólar',
	EURO: 'Retorna o valor do euro',
	LIBRA: 'Retorna o valor da libra',
	DOLAR_AUSTRALIANO: 'Retorna o valor do dólar australiano',
	DOLAR_CANADENSE: 'Retorna o valor do dólar canadence',
	PERDEMO: 'Num ganhamo',
	DISTORCER: 'Distorce aleatoriamente uma imagem dada'
}


def fetch_league_name(command):
	return command.replace(LEAGUE_OPGG, '')


def separate(command):
	return command.split(' ')[1:]


if __name__ == '__main__':
	pass
