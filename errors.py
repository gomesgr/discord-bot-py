from handler import send_message
from discord import Embed, Colour


async def lol_error(ctx, exception, logger, type_ex):
    message = f'Argumento *<nickname>* é necessário para dar continuidade\nExemplo: {ctx.message.content} *<nickname>*'
    e = Embed(color=Colour.red())
    e.title = type_ex
    e.description = message
    logger.error('Error lol: %s', exception, exc_info=False)
    await send_message(ctx, logger, embed=e)


async def coin_error(ctx, exception, logger, type_ex):
    argument = str(exception).split(' ')[0]
    message = f'Argumento *<{argument}>* é necessário para dar continuidade\nExemplo: {ctx.message.content} *<{argument}>*'
    e = Embed(color=Colour.red())
    e.title = type_ex
    e.description = message
    logger.error('Error coin: %s', exception, exc_info=False)
    await send_message(ctx, logger, embed=e)
