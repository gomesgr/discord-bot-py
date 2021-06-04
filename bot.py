import json
import logging
import os
from itertools import cycle
from typing import Optional, List

import discord
from discord.ext import (tasks, commands)
from dotenv import load_dotenv

import bot_constants

load_dotenv('.env')
TKN = os.getenv('BOT_TOKEN')

statuses = cycle(['The game of life', 'With their hearts', 'Soccer'])


def is_me(ctx: commands.Context):
    return str(ctx.author.id) == os.getenv('MY_ID')


def get_prefix(_, message: discord.Message) -> List[str]:
    with open('prefixes.json', 'r') as p:
        prefixes = json.load(p)
    return prefixes[str(message.guild.id)]


diclient = commands.Bot(command_prefix=get_prefix)


@tasks.loop(seconds=10)
async def change_status() -> Optional[None]:
    await diclient.change_presence(activity=discord.Streaming(name='Programando o bot',
                                                              url='https://www.twitch.tv/themrhetch',
                                                              platform='Twitch',
                                                              game='Science & Technology',
                                                              twitch_name='TheMrHetch'))


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


# Cogs
@diclient.command(hidden=True)
@commands.check(is_me)
async def load(_: commands.Context, extension: str) -> Optional[None]:
    diclient.load_extension(f'cogs.{extension}')
    message = f'Cog {extension} loaded from disk'
    logger.info(message)
    print(message)


@diclient.command(hidden=True)
@commands.check(is_me)
async def unload(_: commands.Context, extension: str) -> Optional[None]:
    diclient.unload_extension(f'cogs.{extension}')
    message = f'Cog {extension} unloaded from disk'
    logger.info(message)
    print(message)


@diclient.command(hidden=True)
@commands.check(is_me)
async def reload(ctx: commands.Context, extension: str):
    await unload(ctx, extension)
    await load(ctx, extension)
    await ctx.send(f'Reloaded {extension}')


if __name__ == '__main__':
    # Logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    if not os.path.exists('.logs'):
        os.mkdir('.logs')
    file = logging.FileHandler(
        filename='.logs/bot.log', encoding='utf-8', mode='w')
    file.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(file)
    # End of Logging
    for filename in os.listdir('cogs'):
        if filename[-3:] == '.py':
            diclient.load_extension(f'cogs.{filename[:-3]}')

    diclient.run(TKN)
