from datetime import datetime
from logging import Logger
from typing import (Optional, List)

from discord import (Embed, Colour, File)

import bot_constants
import distort_images as di
import find_rank
from currency import Currency


async def distort(ctx, logger: Logger) -> Optional[None]:
    img: str = ctx.message.attachments[0].url
    print(f'Distorting ({img})')
    d = di.Distort(img)
    d.augment_images()
    with open(di.FOLDER + '/fim.jpg', 'rb') as f:
        send = File(f)
        await send_message(ctx, logger, file=send)
    di.delete_images()
    print('Distortion done')


async def currency_status_fiat(ctx, currency: str, logger: Logger) -> Optional[None]:
    bot_constants.CURRENCIES.get(currency)
    index: int = bot_constants.CURRENCIES[currency]
    c = Currency()
    coin = c.fetch_fiat(index)
    await send_message(ctx, logger, content=f'Valor do {coin}')


async def currency_crypto(ctx, logger: Logger) -> Optional[None]:
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


async def lol(ctx, nickname: List[str], logger: Logger) -> Optional[None]:
    print(f'Looking for {nickname}')
    rank: str = find_rank.find_rank(nickname)
    await send_message(ctx, logger, content=f'Seu ranque é {rank}')


async def ping(ctx, logger: Logger) -> Optional[None]:
    embed = Embed(color=Colour.dark_gold())
    embed.title = 'Pong'
    embed.description = f'{ctx.bot.latency:.3f}ms'
    await send_message(ctx, logger, embed=embed)


async def send_message(ctx, logger: Logger, content: Optional[str] = None, embed: Optional[Embed] = None,
                       file: Optional[File] = None) -> Optional[None]:
    if file is not None:
        await ctx.channel.send(file=file)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            file,
            exc_info=False)
    if embed is not None:
        await ctx.channel.send(embed=embed)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            embed,
            exc_info=False)
    elif content is not None:
        await ctx.channel.send(content)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            content,
            exc_info=False)


if __name__ == '__main__':
    pass
