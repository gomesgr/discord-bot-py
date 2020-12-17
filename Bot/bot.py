import discord
import logging

from handler import Handler

TKN = 'NjAxNTAwNjA1MzUzMjk1ODcz.XTDNFw.WyVwb15x62GhKoOEBYrAuuVdyOQ'

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
