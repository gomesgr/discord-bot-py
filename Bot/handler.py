import os
from sys import path

from discord import Embed

import commands

path.insert(1, 'E:\\Dev\\Python\\Bot\\discord-bot-py\\web')

from currency import Currency
from selenium_lol import LookForRank

HOSTNAME = '1.1.1.1'

class Handler:

	def __init__(self, message_object):
		comm = commands.Commands()
		if message_object.content.startswith(commands.PREFIX):
			self.command = message_object.content
			self.message_object = message_object
			
			# Para ser utilizada na comprehension
			coin = ''.join(comm.separate(self.command))
			
			self.what_to_do = {
				commands.LEAGUE_OPGG: self._opgg_get_rank,
				commands.PING: self._ping_host,
				# Isso daqui é fantástico, mentes brilhantes, 4k QI btw
				next((x for x in commands.CURRENCIES.keys() if x == coin)): self._currency_status
			}
		else:
			raise Exception('Prefixo incorreto')

	async def do(self):
		var = self.command.split()
		
		# Quando a lista da mensagem for maior que 2, passe o parametro para o metodo
		if len(var) > 2:
			await self.what_to_do[var[1]](self.command)
		else:
			await self.what_to_do[var[1]]()

	async def _opgg_get_rank(self, string):
		comm = commands.Commands()
		message_as_list = comm.separate(string)
		print(f'GET RANK: {message_as_list}')
		if message_as_list.pop(0) == commands.LEAGUE_OPGG:
			username = '+'.join(message_as_list)
			look_for = LookForRank(username)
			rank = next(look_for.init())
		await self.message_object.channel.send(f'Seu rank atual : "{rank}"')
	
	async def _ping_host(self):
		import random
		rnd = random.randint(100, 1000)
		embed = Embed(color=Embed.Empty)
		embed.title = 'Pyong li'
		embed.description = rnd
		await self.message_object.channel.send(embed=embed)

	async def _currency_status(self):
		comm = commands.Commands()
		coin = ''.join(comm.separate(self.command))
		commands.CURRENCIES.get(coin)
		command = comm.separate(self.command)
		command = ''.join(command)
		index = commands.CURRENCIES[command]
		currency = Currency()
		fin = next(currency.fetch(index))
		await self.message_object.channel.send(f'Valor do {fin}')

