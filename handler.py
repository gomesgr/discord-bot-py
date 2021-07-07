from logging import Logger
from typing import (Optional)

from discord import (Embed, File, Message)

import distort_images as di
import json


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


async def send_message(ctx, logger: Logger, content: Optional[str] = None, embed: Optional[Embed] = None, file: Optional[File] = None, emojis: Optional[bool] = False) -> Optional[Message]:
    if file is not None:
        message = await ctx.channel.send(file=file)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            file,
            exc_info=False)
    elif embed is not None and not emojis:
        message = await ctx.channel.send(embed=embed)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            embed,
            exc_info=False)
    elif content is not None:
        message = await ctx.channel.send(content)
        logger.info(
            'Message sent on %s: %s',
            ctx.channel,
            content,
            exc_info=False)
    elif embed is not None:
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


async def delete_message(message: Message, logger: Logger):
    await message.delete()
    logger.info(f'Message <{message.id}> deleted ')


async def add_reaction(msg: Message, reaction: str):
    await msg.add_reaction(reaction)


def dump_json(filename: str, content):
    with open(filename, 'w') as f:
        json.dump(content, f, indent=4)


def load_json(filename: str):
    with open(filename, 'r') as f:
        js = json.load(f)
    return js


if __name__ == '__main__':
    pass
