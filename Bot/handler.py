import os

from sys import path
from discord import Embed
from discord import Colour

path.insert(1, 'E:\\Dev\\Python\\Selenium')

from selenium_lol import LookForRank
import commands

HOSTNAME = '1.1.1.1'

class Handler:

	def __init__(self, message_object):
		self.command = message_object.content
		self.message_object = message_object
		self.what_to_do = {
			commands.LEAGUE_OPGG: self._opgg_get_rank,
			commands.PING: self._ping_host
		}

	async def do(self):
		var = self.command.split()
		if len(var) > 2:
			await self.what_to_do[var[1]](self.command)
		else:
			await self.what_to_do[var[1]]()

	async def _opgg_get_rank(self, string):
		comm = commands.Commands()
		messages = comm.separate(string)
		if messages.pop(0).startswith(comm.prefix):
			if messages.pop(0) == commands.LEAGUE_OPGG:
				username = '+'.join(messages)
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
		