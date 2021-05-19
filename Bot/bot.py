import discord
import logging
from os import getenv

from dotenv import load_dotenv
from handler import Handler

import commands

load_dotenv('E:\\Dev\\Python\\Bot\\discord-bot-py\\.env')
TKN = getenv('BOT_TOKEN')

client = discord.Client()


class DiscordClient(discord.Client):
	def __init__(self, logger, *, loop=None, **options):
		super().__init__()
		self.logger = logger


	async def on_ready(self):
		await client.change_presence(activity=discord.Game(name='Jogo da Vida'))
		login_str = f'Logado como {client.user}'
		self.logger.info(login_str)
		print(login_str)


	async def on_message(self, ctx):
		if ctx.content.startswith(commands.PREFIX) and not ctx.author.bot:
			await Handler(ctx, self.logger).do()
		

if __name__ == '__main__':
	# Logging
	logger = logging.getLogger('discord')
	logger.setLevel(logging.INFO)
	file = logging.FileHandler(filename='Bot/.logs/bot.log', encoding='utf-8', mode='w')
	file.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(file)
	# End of Logging
	client = DiscordClient(logger)
	client.run(TKN)
