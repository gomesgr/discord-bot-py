from typing import (Optional, List)

from datetime import datetime
from discord import (Embed, Colour, File, Client, Message)
from logging import Logger
import bot_constants
import distort_images as di
import find_rank
from currency import Currency


async def distort(ctx, logger: Optional[Logger]) -> Optional[None]:
    """
            Distorts the given image and displays it on current discord's text channel
    """
    img: str = ctx.message.attachments[0].url
    print(f'Distorting ({img})')
    d = di.Distort(img)
    d.augment_images()
    with open(di.FOLDER + '/fim.jpg', 'rb') as f:
        send = File(f)
        await send_message(ctx, logger, file=send)
    di.delete_images()
    print('Distortion done')


async def currency_status_fiat(ctx, moeda, logger: Optional[Logger]) -> Optional[None]:
    """
            Method that returns the currency from the brazilian real
    """
    bot_constants.CURRENCIES.get(moeda)
    index: int = bot_constants.CURRENCIES[moeda]
    currency = Currency()
    coin = currency.fetch_fiat(index)
    await send_message(ctx, logger, content=f'Valor do {coin}')


async def currency_crypto(ctx, logger: Optional[Logger]) -> Optional[None]:
    c = Currency()
    df = c.fetch_crypto()

    e = Embed(color=Colour.dark_purple())
    e.title = 'Valor das Criptomoedas'
    e.set_author(name='CoinMarketCap',
                 url='https://coinmarketcap.com/pt-br/')
    for _, name, price in df.itertuples():
        e.add_field(name=name, value=price, inline=False)

    e.set_footer(text=str(datetime.now()))
    await send_message(ctx, logger, embed=e)


async def lol(ctx, nickname: List[str], logger: Optional[Logger]) -> Optional[None]:
    print(f'Looking for {nickname}')
    rank: str = find_rank.find_rank(nickname)
    await send_message(ctx, logger, content=f'Seu ranque é {rank}')


async def ping(ctx, logger: Optional[Logger]) -> Optional[None]:
    embed = Embed(color=Colour.dark_gold())
    embed.title = 'Pong'
    embed.description = f'{ctx.bot.latency:.3f}ms'
    await send_message(ctx, logger, embed=embed)


async def send_message(ctx, logger: Optional[Logger], content: Optional[str] = None, embed: Optional[Embed] = None,
                       file: Optional[File] = None) -> Optional[None]:
    if file is not None:
        await ctx.channel.send(file=file)
        logger.info('Message sent on %s: %s', ctx.channel, file, exc_info=0)
    if embed is not None:
        await ctx.channel.send(embed=embed)
        logger.info('Message sent on %s: %s', ctx.channel, embed, exc_info=0)
    elif content is not None:
        await ctx.channel.send(content)
        logger.info('Message sent on %s: %s', ctx.channel, content, exc_info=0)


if __name__ == '__main__':
    pass
