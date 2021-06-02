from datetime import datetime
from logging import Logger
from typing import (Optional, List)

from discord import (Embed, Colour, File)

import bot_constants
import distort_images as di


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


async def lol(ctx, nickname: List[str], logger: Logger) -> Optional[None]:
    
    rank: str = find_rank.find_rank(nickname)
    await send_message(ctx, logger, content=f'Seu ranque é {rank}')


async def ping(ctx, logger: Logger) -> Optional[None]:
    
    await send_message(ctx, logger, embed=embed)


async def send_message(ctx, logger: Logger, content: Optional[str] = None, embed: Optional[Embed] = None, file: Optional[File] = None) -> Optional[None]:
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
