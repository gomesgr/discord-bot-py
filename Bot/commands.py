# Constants
LEAGUE_OPGG = '-opgg'
PING = '-ping'
EMBED_TEST = '-eb'

# Prefixo
PREFIX = '$kt'

# Currency
DOLAR = '-dolar'
EURO = '-euro'
LIBRA = '-libra'
DOLAR_AUSTRALIANO = '-dolara'
DOLAR_CANADENSE = '-dolarc'

# Crypto
CRYPTO = '-cry'

CURRENCIES = {
    DOLAR: 0,
    EURO: 1,
    LIBRA: 2,
    DOLAR_AUSTRALIANO: 3,
    DOLAR_CANADENSE: 4
}


def fetch_league_name(command):
    return command.replace(LEAGUE_OPGG, '')


def separate(command):
    return command.split(' ')[1:]


if __name__ == '__main__':
    pass
