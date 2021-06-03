from discord.ext import commands
from logging import getLogger
import bot_constants
import handler
from typing import List
from bs4 import BeautifulSoup
from urllib.request import urlopen
from discord import Embed, Colour

logger = getLogger('discord')


class LoLRank:
    def __init__(self, nickname: List[str]):
        self.ranks = {
            'Iron': 'Ferro',
            'Bronze': 'Bronze',
            'Silver': 'Prata',
            'Gold': 'Ouro',
            'Platinum': 'Platina',
            'Diamond': 'Diamante',
            'Master': 'Mestre',
            'Grandmaster': 'Grão-Mestre',
            'Challenger': 'Desafiante'}
        self.nickname = '%20'.join(nickname)
        self.url = f'https://u.gg/lol/profile/br1/{self.nickname}'

    def find(self) -> str:
        bs = BeautifulSoup(urlopen(self.url).read(), 'lxml')
        full_content = bs.title(string=True)[0]
        spl: List[str] = full_content.split(' ')

        rank: List[str] = []

        for x in spl:
            if x in self.ranks.keys():
                print(self.ranks.get(x))
                rank.append(str(self.ranks.get(x)))
            if x.isnumeric():
                rank.append(x)
                break
        return ' '.join(rank)


class Rank(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        message = 'Cog Rank ready'
        logger.info(message)
        print(message)

    @commands.command(name=bot_constants.LOL,
                      aliases=bot_constants.LOL_ALIASES,
                      description='Retorna o ranque do nickname passado no League of Legends',
                      brief=bot_constants.DIC_CMD[bot_constants.LOL])
    async def lol(self, ctx: commands.Context, *nickname: str):
        print(f'Looking for {nickname}')
        lrank = LoLRank(nickname)
        rank: str = lrank.find()
        await handler.send_message(ctx, logger, content=f'Seu ranque é {rank}')

    @lol.error
    async def lol_error(self, ctx: commands.Context, ex):
        if isinstance(ex, commands.errors.CommandInvokeError):
            message = f'Argumento <__nickname__> é necessário para dar continuidade\nExemplo: {ctx.message.content} <__nickname__>'
            embed = Embed(color=Colour.red())
            embed.title = 'Argumento faltando'
            embed.description = message
            logger.error('Error lol: %s', ex, exc_info=False)
            await handler.send_message(ctx, logger, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Rank(bot))
