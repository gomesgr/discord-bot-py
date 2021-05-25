from handler import send_message
from discord import Embed, Colour

async def lol_error(ctx, exception, logger, type_ex):
	argument = str(exception).split(' ')[0]
	message = f'Argumento *<nickname>* é necessário para dar continuidade\nExemplo: {ctx.message.content} *<nickname>*'
	e = Embed(color=Colour.red())
	e.title = type_ex
	e.description = message
	logger.error('Erro: %s', exception, exc_info=1)
	await send_message(ctx, logger, embed=e)