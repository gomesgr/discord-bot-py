from discord import Embed, Colour
from discord.ext import commands
from urllib.request import (urlopen, Request)
from pandas import (read_html, DataFrame)
from re import split
from bot_constants import HEADERS
import bot_constants
import handler
from logging import getLogger
from datetime import datetime


logger = getLogger('discord')


class Currency:
    def __init__(self):
        self.urls = [
            ('https://www.melhorcambio.com/dolar-hoje',
             'Dolar'),
            ('https://www.melhorcambio.com/euro-hoje',
             'Euro'),
            ('https://www.melhorcambio.com/libra-hoje',
             'Libra'),
            ('https://www.melhorcambio.com/dolar-australiano-hoje',
             'Dolar Australiano'),
            ('https://www.melhorcambio.com/dolar-canadense-hoje',
             'Dolar Canadense')]
        self.find = 'class="text-verde"'

    def fetch_fiat(self, index: int) -> str:
        req = Request(self.urls[index][0], headers=HEADERS)
        content = str(urlopen(req).read())
        pos = int(content.index(self.find) + len(self.find))
        return f'{self.urls[index][1]} = ' + \
            str(content[pos - 25: pos - 19]).replace('\"', '')

    def fetch_crypto(self) -> DataFrame:
        url = 'https://coinmarketcap.com/pt-br/'
        df = read_html(url)[0]
        df = df.drop('Unnamed: 0', axis=1)
        df = df.drop('Unnamed: 10', axis=1)
        df = df.dropna(how='all', axis=1)
        df = df[['Nome', 'Preço']]
        df['Nome'] = df['Nome'].apply(lambda x: split('\\d', x, 1)[0])

        return df.head()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currency = Currency()

    @commands.Cog.listener()
    async def on_ready(self):
        message = 'Cog Economy ready'
        print(message)
        logger.info(message)

    @commands.command(name=bot_constants.CRYPTO, aliases=bot_constants.CRYPTO_ALIASES,
                      description='Retorna as 5 mais bem posicionadas criptomoedas no mercado (dados obtidos a partir do site CoinMarketCap)',
                      brief=bot_constants.DIC_CMD[bot_constants.CRYPTO])
    async def cry(self, ctx: commands.Context):
        df = self.currency.fetch_crypto()

        embed = Embed(color=Colour.dark_purple())
        embed.title = 'Valor das Criptomoedas'
        embed.set_author(name='CoinMarketCap',
                         url='https://coinmarketcap.com/pt-br/')
        for _, name, price in df.itertuples():
            embed.add_field(name=name, value=price, inline=False)

        embed.set_footer(text=str(datetime.now()))
        await handler.send_message(ctx, logger, embed=embed)

    @commands.command(name=bot_constants.COIN, aliases=bot_constants.COIN_ALIASES,
                      description='Este comando retornará o valor da moeda no parâmetro dado tendo como referência o REAL (moeda brasileira)',
                      brief=bot_constants.DIC_CMD[bot_constants.COIN])
    async def coin(self, ctx: commands.Context, coin_name: str):
        print('eae')
        bot_constants.CURRENCIES.get(coin_name)
        index: int = bot_constants.CURRENCIES[coin_name]
        coin = self.currency.fetch_fiat(index)
        await handler.send_message(ctx, logger, content=f'Valor do {coin}')

    @coin.error
    async def error(self, ctx: commands.Context, e):
        embed = Embed(color=Colour.red())
        if isinstance(e, commands.errors.MissingRequiredArgument):
            argument = str(e).split(' ')[0]
            message = f'O argumento <__{argument}__> é necessário para dar continuidade\nExemplo: {ctx.message.content} *<{argument}>*'
            embed.title = 'Argumento faltando'
            embed.description = message

        elif isinstance(e, commands.errors.CommandInvokeError):
            argument = str(e).split("'")[1]
            message = f'O argumento <__{argument}__> não existe, utilize um dos abaixo:'
            embed.add_field(name='Moedas', value=str(bot_constants.COIN_LIST))
            embed.title = 'Argumento inválido'
            embed.description = message

        logger.error('Error coin: %s', e, exc_info=False)
        await handler.send_message(ctx, logger, embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
