from logging import getLogger

import bot_constants
import handler
import os
from typing import Optional
from discord import Embed, Message, Colour
from discord.ext import commands
from random import choice

logger = getLogger('discord')


class Jokenpo:
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        self.jokenpo_winning_elements = {'\U0001faa8': '\u2702\uFE0F',
                                         '\U0001f9fb': '\U0001faa8',
                                         '\u2702\uFE0F': '\U0001f9fb'}
        self.msgid = ''

    async def add_message(self) -> Message:
        embed = Embed()
        embed.title = 'Escolha um'
        embed.description = ' '.join(bot_constants.JOKENPO_PIECES)
        msg = await handler.send_message(self.ctx, logger, embed=embed, emojis=True)
        self.msgid = msg.id
        [await handler.add_reaction(msg, reaction) for reaction in bot_constants.JOKENPO_PIECES]
        return await self.ctx.fetch_message(self.msgid)

    async def define_winner(self, message_reaction, message_author, message):
        bot = self.ctx.bot
        if (message_author != bot.user and message_reaction.message.id ==
                message.id and message_reaction.emoji in bot_constants.JOKENPO_PIECES):
            pc_choice, user_choice = choice(
                bot_constants.JOKENPO_PIECES), message_reaction.emoji
            pcwin = user_choice == self.jokenpo_winning_elements[pc_choice]
            userwin = pc_choice == self.jokenpo_winning_elements[user_choice]

            embed = Embed()
            embed.add_field(name='Você escolheu', value=user_choice)
            embed.add_field(name='O computador escolheu', value=pc_choice)

            if userwin and not pcwin:
                embed.title = 'Vencedor'
                embed.description = 'O vencedor foi você!! Parabéns'
                embed.colour = Colour.dark_green()
            elif pcwin and not userwin:
                embed.title = 'Perdedor'
                embed.description = 'O computador levou a melhor dessa vez, tende de novo!'
                embed.colour = Colour.dark_red()
            else:
                embed.title = 'Empate'
                embed.description = 'Mentes brilhantes pensam igual, foi um empate!'
                embed.colour = Colour.orange()
            await handler.edit_message(message, logger, embed=embed)


def not_bot(ctx: commands.Context) -> bool:
    return str(ctx.author.id) != os.getenv('MY_BOT')


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.msg: Optional[Message] = None
        self.jokenpo: Optional[Jokenpo] = None

    @commands.Cog.listener()
    async def on_ready(self):
        message = 'Cog Game ready'
        logger.info(message)
        print(message)

    @commands.command(name=bot_constants.JOKENPO,
                      aliases=bot_constants.JOKENPO_ALIASES)
    async def jokenpo(self, ctx: commands.Context):
        self.jokenpo = Jokenpo(ctx)
        msg = await self.jokenpo.add_message()
        self.msg = msg

    @commands.Cog.listener()
    @commands.check(not_bot)
    async def on_reaction_add(self, reaction, user):
        if self.jokenpo and self.jokenpo.msgid == reaction.message.id:
            await self.jokenpo.define_winner(reaction, user, reaction.message)


def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))
