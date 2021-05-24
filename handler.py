from typing import NoReturn, Optional

from discord import (Embed, Colour, File)

import commands
import distort_images as di
import find_rank
from currency import Currency


class Handler:
    def __init__(self, ctx, logger, client):
        self.message = ctx.content
        self.ctx = ctx
        self.logger = logger
        self.client = client

        self.what_to_do = {
            commands.LEAGUE_OPGG: self._opgg_get_rank,
            commands.PING: self._ping_host,
            commands.CRYPTO: self._currency_crypto,
            commands.COMMANDS: self._get_commands,
            commands.DISTORCER: self._distort
        }

        # Received from discord message
        command = ''.join(
            commands.split_text_with_spaces_using_index(self.message, 1))
        print(f'command {command}')
        """
				Adds the typed coin from discord as key if it exists as a valid coin
				and the `_currency_status_fiat` method as value to be called in
				the `do` method inside the Handler class
		"""
        if command in commands.CURRENCIES.keys():
            self.what_to_do[
                next(x for x in commands.CURRENCIES.keys() if x == command)
            ] = self._currency_status_fiat

    async def do(self) -> NoReturn:
        """
                The first method to be called besides __init__
                Selects what has to be done in the bot by calling
                The methods from what_to_do attribute
        """
        var = self.message.split()
        # When message's list is greater than 2 then pass the parameter as
        # argument to the method
        if len(var) > 2:
            await self.what_to_do[var[1]](' '.join(commands.split_text_with_spaces_using_index(self.message, 2)))
        else:
            await self.what_to_do[var[1]]()

    async def _distort(self) -> NoReturn:
        """
                Distorts the given image and displays it on current discord's text channel
        """
        img = self.ctx.attachments[0].url
        print(f'Distorting ({img})')
        self.logger.info(f'Distorting image from discord: {img}')
        d = di.Distort(img)
        d.augment_images()
        self.logger.info('Reading image')
        with open(di.FOLDER + '/fim.jpg', 'rb') as f:
            send = File(f)
            await self._send_message(file=send)
        self.logger.info('Image sent!')
        di.delete_images()
        self.logger.info('Images deleted')
        print('Distortion done')

    async def _get_commands(self) -> NoReturn:
        """
                Returns to discord's current text channel a list of the bot's commands
        """
        e = Embed(color=Colour.dark_blue())
        e.title = 'Comandos do Bot'
        for c, v in commands.DIC_CMD.items():
            e.add_field(name=c, value=v, inline=False)
        await self._send_message(embed=e)

    async def _opgg_get_rank(self, nickname: str) -> NoReturn:
        print(f'Looking for {nickname}')
        rank = find_rank.find_rank(nickname)
        await self._send_message(f'Seu ranque é {rank}')

    async def _ping_host(self) -> NoReturn:
        embed = Embed(color=Colour.dark_gold())
        embed.title = 'Pong'
        embed.description = f'{self.client.latency:.3f}ms'
        await self._send_message(embed=embed)

    async def _currency_status_fiat(self) -> NoReturn:
        """
                Method that returns the currency from the brazilian real
        """
        command = ''.join(
            commands.split_text_with_spaces_using_index(self.message, 1))
        self.logger.info(f'Getting currency {command}')
        commands.CURRENCIES.get(command)
        index = commands.CURRENCIES[command]
        currency = Currency()
        coin = (currency.fetch_fiat(index))
        await self._send_message(f'Valor do {coin}')

    async def _currency_crypto(self) -> NoReturn:
        from datetime import datetime
        self.logger.info(f'Getting crypto currency')
        c = Currency()
        df = c.fetch_crypto()

        e = Embed(color=Colour.dark_purple())
        e.title = 'Valor das Criptomoedas'
        e.set_author(name='CoinMarketCap',
                     url='https://coinmarketcap.com/pt-br/')

        for _, name, price in df.itertuples():
            e.add_field(name=name, value=price, inline=False)

        e.set_footer(text=str(datetime.now()))
        await self._send_message(embed=e)

    async def _send_message(self, content: Optional[str] = None, embed: Optional[Embed] = None,
                            file: Optional[File] = None) -> NoReturn:
        if file is not None:
            await self.ctx.channel.send(file=file)
        if embed is not None:
            await self.ctx.channel.send(embed=embed)
        elif content is not None:
            await self.ctx.channel.send(content)

        self.logger.info(f'Message sent on {self.ctx.channel}')
        print(f'Message sent on {self.ctx.channel}')


if __name__ == '__main__':
    pass
