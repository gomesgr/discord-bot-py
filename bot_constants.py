# TODO Create class to divide constant types
from typing import List

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
    'Safari/537.3'}

# Constants ; aliases
LOL = 'lol'
LOL_ALIASES = ('l', 'opgg', 'ugg')

PING = 'ping'
PING_ALIASES = ('p', 'pingue')

DISTORT = 'distorcer'
DISTORT_ALIASES = ('dist', 'd')
# Prefixo
PREFIX = 'k'
CHANGE_PREFIX = 'changeprefix'
CHANGE_PREFIX_ALIASES = ('cp', 'changep', 'cprefix')

# Currency
COIN = 'moeda'
COIN_ALIASES = ('coin', 'm')

DOLAR = 'dolar'
EURO = 'euro'
LIBRA = 'libra'
DOLAR_AUSTRALIANO = 'dolara'
DOLAR_CANADENSE = 'dolarc'

COIN_LIST = [DOLAR, EURO, LIBRA, DOLAR_AUSTRALIANO, DOLAR_CANADENSE]

# Crypto
CRYPTO = 'criptomoedas'
CRYPTO_ALIASES = ('c', 'cry')

CURRENCIES = {
    DOLAR: 0,
    EURO: 1,
    LIBRA: 2,
    DOLAR_AUSTRALIANO: 3,
    DOLAR_CANADENSE: 4
}

DIC_CMD = {
    PREFIX: 'Prefixo do Bot',
    PING: 'Retorna a latência do bot',
    LOL: 'Retorna o ranque de um usuario no LoL',
    CRYPTO: 'Retorna o valor de cinco criptomoedas',
    COIN: 'Retorna o valor de uma das moedas',
    DISTORT: 'Distorce aleatoriamente uma imagem dada',
    CHANGE_PREFIX: 'Muda o prefixo do bot'}

# Games
JOKENPO = 'jokenpo'
JOKENPO_ALIASES = ('jk', 'jkp', 'ppt')
JOKENPO_PIECES = ['\U0001faa8', '\U0001f9fb', '\u2702\uFE0F']

# Manga
MANGA_SEARCH = 'mangasearch'
MANGA_SEARCH_ALIASES = ('ms', 'msearch', 'procurarmanga')

# Emojis

RIGHT_WRONG = ['\u2705', '\u274C']

FIRST = '\u23EE\uFE0F'
NEXT = '\u25B6\uFE0F'
PREVIOUS = '\u25C0\uFE0F'
LAST = '\u23ED\uFE0F'

NUMBERS_ONE_TO_FIVE = [
    '1\uFE0F\u20E3',
    '2\uFE0F\u20E3',
    '3\uFE0F\u20E3',
    '4\uFE0F\u20E3',
    '5\uFE0F\u20E3'
]


def split_text_with_spaces_using_index(text: str, index: int) -> List[str]:
    return text.split(' ')[index:]


def fetch_league_name(command: str) -> str:
    return command.replace(LOL, '')


# def separate(command: str) -> List[str]:
# 	return command.split(' ')[1:]


if __name__ == '__main__':
    pass
