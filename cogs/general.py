from discord.ext import commands
from logging import getLogger
import bot_constants
import handler
from discord import (Embed, Colour)

import json

logger = getLogger('discord')


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        message = 'Cog General ready'
        logger.info(message)
        print(message)

    @commands.command(name=bot_constants.PING,
                      aliases=bot_constants.PING_ALIASES,
                      description='Pong!',
                      brief=bot_constants.DIC_CMD[bot_constants.PING])
    async def ping(self, ctx: commands.Context):
        embed = Embed(color=Colour.dark_gold())
        embed.title = 'Pong'
        embed.description = f'{ctx.bot.latency:.3f}ms'
        await handler.send_message(ctx, logger, embed=embed)

    @commands.command(name=bot_constants.CHANGE_PREFIX,
                      aliases=bot_constants.CHANGE_PREFIX_ALIASES,
                      description='Muda o prefixo do bot para um de sua escolha',
                      brief=bot_constants.DIC_CMD[bot_constants.CHANGE_PREFIX])
    async def changeprefix(self, ctx, prefix):
        with open('./prefixes.json', 'r') as p:
            prefixes = json.load(p)
            prefixes[str(ctx.guild.id)] = prefix

        with open('./prefixes.json', 'w') as p:
            json.dump(prefixes, p, indent=4)


def setup(bot: commands.Bot):
    bot.add_cog(General(bot))
