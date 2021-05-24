import discord
import logging
from os import getenv

from dotenv import load_dotenv
from handler import Handler

import commands

load_dotenv('.env')
TKN = getenv('BOT_TOKEN')


class DiscordClient(discord.Client):
    def __init__(self, logger, *, loop=None, **options):
        super().__init__()
        self.logger = logger

    async def on_ready(self):
        await self.change_presence(activity=discord.Streaming(name='Jogo da Vida',
                                                              platform='Twitch',
                                                              url='https://www.twitch.tv/themrhetch', ))
        login_str = f'Logado como {self.user}'
        self.logger.info(login_str)
        print(login_str)

    async def on_message(self, ctx: discord.Message):
        if ctx.content.startswith(commands.PREFIX) and not ctx.author.bot:
            self.logger.info('Initializing Handler object')
            await Handler(ctx, self.logger, self).do()


if __name__ == '__main__':
    # Logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    file = logging.FileHandler(
        filename='.logs/bot.log',
        encoding='utf-8',
        mode='w')
    file.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(file)
    # End of Logging
    client = DiscordClient(logger)
    client.run(TKN)
