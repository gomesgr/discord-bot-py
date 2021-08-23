from discord.ext import commands
from logging import getLogger
from typing import Optional, List

from PIL import Image, ImageFont, ImageDraw

import os

import bot_constants as bc
import handler as hn

logger = getLogger('memes')


class Memes(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self) -> Optional[None]:
        message = "Cog Memes ready"
        logger.info(message)
        print(message)

    @commands.command(name=bc.MEMES_SPONGEBOB,
                      aliases=bc.MEMES_SPONGEBOB_ALIASES)
    async def spongebob(self) -> Optional[None]:
        s = Spongebob()


def setup(bot: commands.Bot) -> Optional[None]:
    bot.add_cog(Memes(bot))


class MemeFather:
    def __init__(
            self,
            content,
            image_src: str,
            fraction: Optional[float] = 0.6,
            font_size: Optional[int] = 1):
        self.content = content
        self.image_src = Image.open(image_src)
        self.fraction = fraction
        self.font_size = font_size
        self.font = ImageFont.truetype('playfair.ttf', self.font_size)


class Spongebob(MemeFather):
    def __init__(self):
        super().__init__()

    def create(self):
        self.fractionate_word()

    def fractionate_word(self):
        strl = List()
        for i, word in enumerate(self.content.split(' ')):
            if i % 3 == 0:
                strl.append('\n')
                strl.append(word)
            else:
                strl.append(word)
        self.content = ' '.join(strl).strip()
        while self.font.getsize(
                self.content)[0] < self.fraction * self.image_src.size[0]:
            self.font_size += 1
            self.font = ImageFont.truetype('playfair.ttf', self.font_size)

    def edit_image(self) -> Optional[None]:
        editable = ImageDraw.Draw(self.image_src)
        editable.text((60, 80), self.content, (0, 0, 0), font=self.font)
        self.image_src.save('result.jpg')
