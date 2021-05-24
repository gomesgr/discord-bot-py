# TODO Create class to divide constant types
from typing import List

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
    'Safari/537.3'}

# Constants
LEAGUE_OPGG = 'lol'
PING = 'ping'
TEST = 't'
COMMANDS = 'c'
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
    DISTORCER: 'Distorce aleatoriamente uma imagem dada'
}


def split_text_with_spaces_using_index(text: str, index: int) -> List[str]:
    return text.split(' ')[index:]


def fetch_league_name(command: str) -> str:
    return command.replace(LEAGUE_OPGG, '')


# def separate(command: str) -> List[str]:
# 	return command.split(' ')[1:]


if __name__ == '__main__':
    pass
