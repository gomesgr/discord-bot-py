from discord.ext import commands
from logging import getLogger
import bot_constants
import handler

logger = getLogger('discord')


class Image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        message = 'Cog Image ready'
        logger.info(message)
        print(message)

    @commands.command(name=bot_constants.DISTORT,
                      aliases=bot_constants.DISTORT_ALIASES,
                      description='Este comando recebe uma imagem anexada a mensagem e a distorce',
                      brief=bot_constants.DIC_CMD[bot_constants.DISTORT])
    async def distort(self, ctx: commands.Context):
    	await handler.distort(ctx, logger)


def setup(bot: commands.Bot):
    bot.add_cog(Image(bot))
