import os
from sys import path
import logging

from discord import (Embed, Colour)

import commands
from time import time

path.insert(1, 'E:\\Dev\\Python\\Bot\\discord-bot-py\\web')
path.insert(2, 'E:\\Dev\\Python\\Bot\\discord-bot-py\\exceptions')

from database import (player_crud, champion_crud)
from currency import Currency
from selenium_lol import LookForRank
from IncorrectPrefixException import IncorrectPrefixException

HOSTNAME = '1.1.1.1'

class Handler:

	def __init__(self, ctx, logger):
		if ctx.content.startswith(commands.PREFIX):
			self.comm = commands.Commands()
			self.message = ctx.content
			self.ctx = ctx	
			self.logger = logger

			self.what_to_do = {
				commands.LEAGUE_OPGG: self._opgg_get_rank,
				commands.PING: self._ping_host,
			}
			
			coin = ''.join(self.comm.separate(self.message))
			if coin in commands.CURRENCIES.keys():
				self.what_to_do[next((x for x in commands.CURRENCIES.keys() if x == coin))] = self._currency_status

		else:
			raise IncorrectPrefixException('Prefixo incorreto')

	async def do(self):
		var = self.message.split()
		
		# When message's list is greater than 2 then pass the parameter as argument to the method
		if len(var) > 2:
			await self.what_to_do[var[1]](self.message)
		else:
			await self.what_to_do[var[1]]()
	
	async def _opgg_get_rank(self, string):
		""" Method to return the player's rank from league of legends

		Args:
			string (str): The message itself to be formatted in the method
		"""
		message_as_list = self.comm.separate(string)
		if message_as_list.pop(0) == commands.LEAGUE_OPGG:
			username_for_crawl = '+'.join(message_as_list) ; username_for_db = ' '.join(message_as_list)
			self.logger.info(f'GET RANK: {username_for_db}\n')

			pdao = player_crud.PlayerDAO()
			fetched_player = pdao.fetch(username_for_db)
			look_for = LookForRank(username_for_crawl)

			# If the time between updates is greater than 1 hour then, collect the rank with selenium
			# else, fetch from firebase database
			if type(fetched_player) == type(None) or int((time() - fetched_player['created_at'])) >= 3600: 
				rank = look_for.init()
				pl = player_crud.Player(username_for_db, rank)
				pdao.save(pl)
				embed = self._get_embed('Seu rank atual', rank)
				# embed = self._live_winrate(embed, username_for_crawl)
			else:
				embed = self._get_embed('Seu rank atual', fetched_player['rank'])
				# embed = self._live_winrate(embed, username_for_crawl)
			await self._send_message(embed=embed)
	
	async def _ping_host(self):
		import random
		rnd = random.randint(100, 1000)
		embed = self._get_embed('Pyong li', f'Não quer dizer nada\n{rnd}ms', Colour.dark_purple())
		await self._send_message(embed=embed)

	async def _currency_status(self):
		""" Method that returns the currency from the brazilian real """
		coin = ''.join(self.comm.separate(self.message))
		self.logger.info(f'Getting currency {coin}')
		commands.CURRENCIES.get(coin)
		command = ''.join(self.comm.separate(self.message))
		index = commands.CURRENCIES[command]
		currency = Currency()
		fin = (currency.fetch(index))
		await self._send_message(f'Valor do {fin}')

	""" # Desabilitado ate segunda ordem, muito lento utilizando SELENIUM
	def _live_winrate(self, eb, username):
		champions_live = selenium_lol_live_game.get_live_champions(username)
		if (champions_live != None):
			winrates_per_champ = selenium_lol_stats.fill_dict()
			winrates_game = selenium_lol_stats.fill_winrates(winrates_per_champ, username)
			eb.add_field(name='Partida ao vivo', value=f'Blue: {winrates_game[0]} Red: {winrates_game[1]}', inline=False)
		return eb
	"""

	def _get_embed(self, title, desc, color=Embed.Empty):
		eb = Embed(colour=color)
		eb.title = title
		eb.description = desc
		return eb
	
	async def _send_message(self, content=None, embed=None):
		if embed != None:
			await self.ctx.channel.send(embed=embed)
		if content != None:
			await self.ctx.channel.send(content)

if __name__ == '__main__':
	pass