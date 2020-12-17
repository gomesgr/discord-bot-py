import discord
import logging
import os

from dotenv import load_dotenv

from handler import Handler

load_dotenv('E:\\Dev\\Python\\Bot\\discord-bot-py\\.env')

TKN = os.getenv('BOT_TOKEN')

class MyClient(discord.Client):
	async def on_ready(self):
		await self.change_presence(activity=discord.Game(name='Jogo da Vida'))
		print(f'Logado como {self.user}')
	
	async def on_message(self, message):
		hnd = Handler(message)
		await hnd.do()
		
if __name__ == '__main__':
	
	# Logging
	logger = logging.getLogger('discord')
	logger.setLevel(logging.DEBUG)
	file = logging.FileHandler(filename='Bot/logs/bot.log', encoding='utf-8', mode='w')
	file.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(file)
	# End of Logging

	client = MyClient()
	client.run(TKN)
