import discord
import logging
from os import getenv

from dotenv import load_dotenv
from handler import Handler
from typing import NoReturn

import commands

load_dotenv('.env')
TKN = getenv('BOT_TOKEN')


class DiscordClient(discord.Client):
    def __init__(self, logger, *, loop=None, **options):
        super().__init__()
        self.logger = logger

    async def on_ready(self) -> NoReturn:
        await self.change_presence(activity=discord.Streaming(name='Jogo da Vida',
                                                              platform='Twitch',
                                                              url='https://www.twitch.tv/themrhetch', ))
        login_str = f'Logado como {self.user}'
        self.logger.info(login_str)
        print(login_str)
        # Latency between a HEARTBEAT and a HEARTBEAT_ACK in seconds.
        # This could be referred to as the Discord Voice WebSocket
        # latency and is an analogue of #user’s voice latencies as
        # seen in the Discord client. (discord.py docs)
        self.logger.info(f'Latency: {self.latency:.4f}s')

    async def on_message(self, message: discord.Message) -> NoReturn:
        if message.content.startswith(commands.PREFIX) and not message.author.bot:
            self.logger.info('Initializing Handler object')
            await Handler(message, self.logger, self).do()


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
