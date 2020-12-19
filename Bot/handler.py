import os
from sys import path

from discord import (Embed, Colour)

import commands
from time import time

path.insert(1, 'E:\\Dev\\Python\\Bot\\discord-bot-py\\web')

import rank_crud
from currency import Currency
from selenium_lol import LookForRank

HOSTNAME = '1.1.1.1'

class Handler:

	def __init__(self, message_object):
		if message_object.content.startswith(commands.PREFIX):
			self.comm = commands.Commands()
			self.message = message_object.content
			self.message_object = message_object
			
			# Para ser utilizada na comprehension
			coin = ''.join(self.comm.separate(self.message))

			self.what_to_do = {
				commands.LEAGUE_OPGG: self._opgg_get_rank,
				commands.PING: self._ping_host,
			}

			if coin in commands.CURRENCIES.keys():
				self.what_to_do[next((x for x in commands.CURRENCIES.keys() if x == coin))] = self._currency_status

		else:
			raise Exception('Prefixo incorreto')

	async def do(self):
		var = self.message.split()
		
		# Quando a lista da mensagem for maior que 2, passe o parametro para o metodo
		if len(var) > 2:
			await self.what_to_do[var[1]](self.message)
		else:
			await self.what_to_do[var[1]]()
	
	async def _opgg_get_rank(self, string):
		""" Método para retornar o rank de um jogador no league of legends

		Args:
			string (str): A mensagem que será recebida para ser cortada neste método
		"""
		message_as_list = self.comm.separate(string)
		print(f'GET RANK: {message_as_list[1:]}')
		if message_as_list.pop(0) == commands.LEAGUE_OPGG:
			username_for_crawl = '+'.join(message_as_list)
			username_for_db = ' '.join(message_as_list)

			pdao = rank_crud.PlayerDAO()
			fetched_player = pdao.fetch(username_for_db)
			
			# Se o tempo entre a atualizadao dor rank for maior que 10 segundos
			look_for = LookForRank(username_for_crawl)
			if type(fetched_player) == type(None) or int((time() - fetched_player['created_at'])) >= 3600: 
				rank = look_for.init()
				pl = rank_crud.Player(username_for_db, rank)
				pdao.save(pl)
				embed = self._get_embed('Seu rank atual', rank)
				
				print('================================')
				print(f'Criando/atualizando valor de {pl}')
				print('================================')
			else:
				embed = self._get_embed('Seu rank atual', fetched_player['rank'])
			await self.message_object.channel.send(embed=embed)
	
	async def _ping_host(self):
		import random
		rnd = random.randint(100, 1000)
		embed = self._get_embed('Pyong li', f'Não quer dizer nada\n{rnd}ms', Colour.dark_purple())
		await self.message_object.channel.send(embed=embed)

	async def _currency_status(self):
		""" Método para retornar o valor da moeda diginada nas mensagens
		"""		
		coin = ''.join(self.comm.separate(self.message))
		commands.CURRENCIES.get(coin)
		command = ''.join(self.comm.separate(self.message))
		index = commands.CURRENCIES[command]
		currency = Currency()
		fin = (currency.fetch(index))
		await self.message_object.channel.send(f'Valor do {fin}')

	def _get_embed(self, title, desc, color=Embed.Empty):
		eb = Embed(colour=color)
		eb.title = title
		eb.description = desc
		return eb

