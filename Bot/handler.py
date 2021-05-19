from currency import Currency
from discord import (Embed, Colour)

import commands
import find_rank


class Handler:
	def __init__(self, ctx, logger):
		self.comm = commands
		self.message = ctx.content
		self.ctx = ctx
		self.logger = logger

		self.what_to_do = {
			commands.LEAGUE_OPGG: self._opgg_get_rank,
			commands.PING: self._ping_host,
			commands.CRYPTO: self._currency_crypto
		}

		# Received from discord message
		coin = ''.join(self.comm.separate(self.message))

		if coin in commands.CURRENCIES.keys():
			self.what_to_do[next(x for x in commands.CURRENCIES.keys() if x == coin)] = self._currency_status_fiat

	
	async def do(self):
		var = self.message.split()
		# When message's list is greater than 2 then pass the parameter as argument to the method
		if len(var) > 2:
			await self.what_to_do[var[1]](' '.join(self.message.split(' ')[2:]))
		else:
			await self.what_to_do[var[1]]()

	
	async def _opgg_get_rank(self, nickname):
		rank = find_rank.find_rank(nickname)
		await self._send_message(f'Seu ranque é {rank}')

	
	async def _ping_host(self):
		from random import randint
		rnd = randint(100, 1000)
		embed = self._get_embed('Pyong li', f'Não quer dizer nada\n{rnd}ms', Colour.dark_purple())
		await self._send_message(embed=embed)

	
	async def _currency_status_fiat(self):
		""" Method that returns the currency from the brazilian real """
		coin = ''.join(self.comm.separate(self.message))
		self.logger.info(f'Getting currency {coin}')
		commands.CURRENCIES.get(coin)
		command = ''.join(self.comm.separate(self.message))
		index = commands.CURRENCIES[command]
		currency = Currency()
		fin = (currency.fetch_fiat(index))
		await self._send_message(f'Valor do {fin}')

	
	async def _currency_crypto(self):
		self.logger.info(f'Getting crypto currency')
		c = Currency()
		df = c.fetch_crypto()
		await self._send_message(df)


	def _get_embed(self, title, desc, color=Embed.Empty):
		eb = Embed(colour=color)
		eb.title = title
		eb.description = desc
		return eb


	async def _send_message(self, content=None, embed=None):
		if embed is not None:
			await self.ctx.channel.send(embed=embed)
		elif content is not None:
			await self.ctx.channel.send(content)


if __name__ == '__main__':
	pass
