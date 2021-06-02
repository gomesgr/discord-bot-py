import json
import logging
from itertools import cycle
import os
from typing import Optional, List

import discord
from discord.ext import (tasks, commands)
from dotenv import load_dotenv

import bot_constants
import errors
import handler

load_dotenv('.env')
TKN = os.getenv('BOT_TOKEN')

statuses = cycle(['The game of life', 'With their hearts', 'Soccer'])


def get_prefix(_, message: discord.Message) -> List[str]:
    with open('prefixes.json', 'r') as p:
        prefixes = json.load(p)
    return prefixes[str(message.guild.id)]


diclient = commands.Bot(command_prefix=get_prefix)


@tasks.loop(seconds=10)
async def change_status() -> Optional[None]:
    await diclient.change_presence(activity=discord.Game(next(statuses)))


@diclient.event
async def on_ready() -> Optional[None]:
    login_str = f'Logado como {diclient.user}'
    logger.info(login_str)
    print(login_str)

    logger.info(f'Latency: {diclient.latency:.4f}s')
    change_status.start()


@diclient.event
async def on_guild_join(guild) -> Optional[None]:
    with open('prefixes.json', 'r') as p:
        prefixes = json.load(p)

    prefixes[str(guild.id)] = bot_constants.PREFIX

    with open('prefixes.json', 'w') as p:
        json.dump(prefixes, p, indent=4)


"""Commands"""


@diclient.command(name=bot_constants.CHANGE_PREFIX,
                  aliases=bot_constants.CHANGE_PREFIX_ALIASES,
                  description='Muda o prefixo do bot para um de sua escolha',
                  brief=bot_constants.DIC_CMD[bot_constants.CHANGE_PREFIX])
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as p:
        prefixes = json.load(p)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as p:
        json.dump(prefixes, p, indent=4)


# PING
@diclient.command(name=bot_constants.PING,
                  aliases=bot_constants.PING_ALIASES,
                  description='Pong!',
                  brief=bot_constants.DIC_CMD[bot_constants.PING])
async def ping(ctx: commands.Context) -> Optional[None]:
    await handler.ping(ctx, logger)


# LOL



# DISTORT
@diclient.command(name=bot_constants.DISTORT,
                  aliases=bot_constants.DISTORT_ALIASES,
                  description='Este comando recebe uma imagem anexada a mensagem e a distorce',
                  brief=bot_constants.DIC_CMD[bot_constants.DISTORT])
async def distort(ctx: commands.Context) -> Optional[None]:
    await handler.distort(ctx, logger)


# Cogs
@diclient.command()
async def load(ctx: commands.Context, extension: str) -> Optional[None]:
    if str(ctx.author.id) == os.getenv('MY_ID'):
        diclient.load_extension(f'cogs.{extension}')
        message = f'Cog {extension} loaded from disk'
        logger.info(message); print(message)

@diclient.command()
async def unload(ctx: commands.Context, extension: str) -> Optional[None]:
    if str(ctx.author.id) == os.getenv('MY_ID'):
        diclient.unload_extension(f'cogs.{extension}')
        message = f'Cog {extension} unloaded from disk'
        logger.info(message); print(message)


if __name__ == '__main__':
    # Logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    file = logging.FileHandler(
        filename='.logs/bot.log', encoding='utf-8', mode='w')
    file.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(file)
    # End of Logging
    for filename in os.listdir('./cogs'):
        if filename[-3:] =='.py':
            diclient.load_extension(f'cogs.{filename[:-3]}')

    diclient.run(TKN)
