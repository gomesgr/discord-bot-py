from logging import Logger
from typing import (Optional)

from discord import (Embed, File, Message)

import distort_images as di
from logging import Logger
from typing import (Optional)

from discord import (Embed, File, Message)

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


async def send_message(ctx, logger: Logger, content: Optional[str] = None, embed: Optional[Embed] = None, file: Optional[File] = None, emojis: Optional[bool] = None) -> Optional[Message]:
    if file is not None:
        await ctx.channel.send(file=file)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            file,
            exc_info=False)
    elif embed is not None and not emojis:
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
    elif embed is not None and emojis:
        message = await ctx.send(embed=embed)
        print(message)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            embed,
            exc_info=False)
        return message


async def edit_message(message: Message, logger: Logger, content: Optional[str] = None, embed: Optional[Embed] = None, file: Optional[File] = None) -> Optional[None]:
    if embed is not None:
        logger.info('Message %s edited on %s', str(message.id), message.channel, exc_info=False)
        await message.edit(embed=embed)


async def add_reaction(msg: Message, reaction: str):
    await msg.add_reaction(reaction)


if __name__ == '__main__':
    pass
