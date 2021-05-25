import json
import logging
from itertools import cycle
from os import getenv
from typing import Optional, List

import discord
from discord.ext import (tasks, commands)
from dotenv import load_dotenv

import bot_constants
import handler

load_dotenv('.env')
TKN = getenv('BOT_TOKEN')

statuses = cycle(['The game of life', 'With their hearts', 'Soccer'])


def get_prefix(client, message) -> List[str]:
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


@diclient.command(name=bot_constants.PING,
                  aliases=bot_constants.PING_ALIASES,
                  description='Pong!',
                  brief=bot_constants.DIC_CMD[bot_constants.PING])
async def ping(ctx: commands.Context) -> Optional[None]:
    await handler.ping(ctx, logger)


@diclient.command(name=bot_constants.LOL,
                  aliases=bot_constants.LOL_ALIASES,
                  description='Retorna o ranque do nickname passado no League of Legends',
                  brief=bot_constants.DIC_CMD[bot_constants.LOL])
async def lol(ctx: commands.Context, nickname: str) -> Optional[None]:
    await handler.lol(ctx, nickname, logger)


@diclient.command(name=bot_constants.CRYPTO, aliases=bot_constants.CRYPTO_ALIASES,
                  description='Retorna as 5 mais bem posicionadas criptomoedas no mercado (dados obtidos a partir do site CoinMarketCap)',
                  brief=bot_constants.DIC_CMD[bot_constants.CRYPTO])
async def cry(ctx: commands.Context) -> Optional[None]:
    await handler.currency_crypto(ctx, logger)


@diclient.command(name=bot_constants.COIN, aliases=bot_constants.COIN_ALIASES,
                  description='Este comando retornará o valor da moeda no parâmetro dado tendo como referência o REAL (moeda brasileira)',
                  brief=bot_constants.DIC_CMD[bot_constants.COIN])
async def coin(ctx: commands.Context, coin_name: str) -> Optional[None]:
    await handler.currency_status_fiat(ctx, coin_name, logger)


@diclient.command(name=bot_constants.DISTORT,
                  aliases=bot_constants.DISTORT_ALIASES,
                  description='Este comando recebe uma imagem anexada a mensagem e a distorce',
                  brief=bot_constants.DIC_CMD[bot_constants.DISTORT])
async def distort(ctx: commands.Context) -> Optional[None]:
    await handler.distort(ctx, logger)


"""Error handling"""


@lol.error
async def lol_error(ctx: commands.Context, exception) -> Optional[None]:
    if isinstance(exception, commands.errors.MissingRequiredArgument):
        await handler.on_error(ctx, exception, logger, commands.errors.MissingRequiredArgument)

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
    diclient.run(TKN)
