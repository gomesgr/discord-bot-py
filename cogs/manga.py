import os
from logging import getLogger
from typing import Optional, List, Dict, Tuple, Union
import requests
import json

import handler
import bot_constants
import pandas as pd
from discord.ext import commands
from discord import TextChannel, Embed, PermissionOverwrite, utils

logger = getLogger('manga')


def not_bot(user) -> bool:
	return str(user.id) != os.getenv('MY_BOT')


class Manga(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.msg_embed_cover_id = ''
		self.ctx: Optional[commands.Context] = None
		self.count = 0
		self.md: Mangadownloader = Mangadownloader()
		self.manga: Dict[str, str] = {}
		self.manga_df: pd.DataFrame = pd.DataFrame()
		self.previous_manga_df = pd.DataFrame()
		self.manga_page = 0
		self.users_using: Dict[str, int] = dict()
		self.items = 5

	@commands.Cog.listener()
	async def on_ready(self):
		message = 'Cog Manga ready'
		print(message)
		logger.info(message)

	@commands.command(name=bot_constants.MANGA_SEARCH, aliases=bot_constants.MANGA_SEARCH_ALIASES)
	async def mangasearch(self, ctx: commands.Context, *manga_name: str):
		self.count = 0
		manga_name = list(manga_name)
		self.manga['uuid'], self.manga['name'], self.manga['cover_url'] = self.md.search(manga_name)
		embed = Embed()
		print(self.manga['cover_url'])
		embed.set_image(url=self.manga['cover_url'])
		embed.title = 'Capa'
		embed.set_footer(text=self.manga['name'])
		embed.description = 'É esse o mangá que você está procurando?'
		msg = await handler.send_message(ctx, logger, embed=embed, emojis=True)
		self.msg_embed_cover_id = msg.id
		self.ctx = ctx
		[await handler.add_reaction(msg, reaction) for reaction in bot_constants.RIGHT_WRONG]

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if not user.bot:
			if self.count == 0:
				if self.msg_embed_cover_id == reaction.message.id:
					if reaction.emoji == bot_constants.RIGHT_WRONG[0]:
						self.count = 1
						await self._init_search()
						return

			with open('text_channels.json', 'r') as f:
				channels = json.load(f)

			if str(reaction.message.channel.id) == channels[str(reaction.message.guild.id)][str(user.id)]:
				# NEXT
				if reaction.emoji == bot_constants.NEXT:
					embed = Embed()
					embed.title = 'Escolha o capitulo abaixo:'
					self.manga_page += 1
					self.items += 5
					print('next')
					c = 0
					for x in self.manga_df.iloc[self.items - 5:self.items].itertuples():
						embed.add_field(name=bot_constants.NUMBERS_ONE_TO_FIVE[c], value=f'{x.chapter:.1f}', inline=False)
						c += 1
					await reaction.message.edit(embed=embed)

				# PREVIOUS
				elif reaction.emoji == bot_constants.PREVIOUS and self.manga_page >= 1:
					embed = Embed()
					embed.title = 'Escolha o capitulo abaixo:'
					self.manga_page -= 1
					self.items -= 5
					print('prev')
					c = 0
					for x in self.manga_df.iloc[self.items - 5:self.items].itertuples():
						embed.add_field(name=bot_constants.NUMBERS_ONE_TO_FIVE[c], value=f'{x.chapter:.1f}', inline=False)
						c += 1
					await reaction.message.edit(embed=embed)
				print(self.manga_page)

	async def _init_search(self):
		from string import whitespace
		"""
			Starts iteration over manga chapters
		"""
		if self.count == 1:
			self.manga_df = self.md.init(self.manga['name'], self.manga['uuid'])
			created_channel = await self._create_text_channel()
			embed = Embed()
			embed.title = 'Escolha o capitulo abaixo:'

			first_five = [f'{x.chapter:.1f}' for x in self.manga_df.head().itertuples()]

			for i in range(5):
				embed.add_field(name=bot_constants.NUMBERS_ONE_TO_FIVE[i], value=first_five[i], inline=False)

			message = await created_channel.send(embed=embed)
			await message.add_reaction(bot_constants.PREVIOUS)
			await message.add_reaction(bot_constants.NEXT)
			[await message.add_reaction(v) for v in bot_constants.NUMBERS_ONE_TO_FIVE]
			# await self._change_context(created_channel)

	async def _change_context(self, channel):
		pass

	async def _create_text_channel(self):
		"""
			Creates the user-related text-channel
		"""
		with open('text_channels.json', 'r') as f:
			channels = json.load(f)

		author = self.ctx.author

		self.users_using[str(author.id)] = 0

		channel: TextChannel = await self.ctx.guild.create_text_channel(f'{self.manga["name"]}-{author.name}')
		ow = PermissionOverwrite()
		ow.send_messages = False
		ow.read_messages = True
		await channel.set_permissions(author, overwrite=ow)

		default_role = utils.get(self.ctx.guild.roles, name='@everyone')

		ow.read_messages = False
		await channel.set_permissions(default_role, overwrite=ow)

		channels[str(self.ctx.guild.id)][str(author.id)] = str(channel.id)

		with open('text_channels.json', 'w') as f:
			json.dump(channels, f, indent=4)

		return channel

		# e = discord.Embed()
		# for v in self.manga_df.head().itertuples():
		# 	e.add_field(name='Capitulo', value=f'{v.chapter:.1f}', inline=False)
		# await channel.send(embed=e)


class Mangadownloader:
	"""
		Downloads given manga chapters using maximum quality (data) from mangadex api. (limited to 100 chapters)
	"""

	def __init__(self):
		self.manga_name: Optional[str] = ''
		self.manga_id: Optional[str] = ''

		self.json_chapters: Dict[str] = {}
		self.df: Optional[pd.DataFrame] = pd.DataFrame()
		self.chapters: List[str] = []

		self.apiurl = 'https://api.mangadex.org'
		self.final_url = 'https://uploads.mangadex.org/data/{0}/{1}'
		self.full_url: Optional[str] = ''

		self.cover_find_url = 'https://api.mangadex.org/cover?manga[]={0}&order[volume]=desc&limit=1'
		self.cover_final_url = 'https://uploads.mangadex.org/covers/{0}/{1}'
		self.cover_art = ''
		self.cover_art_file = ''

	def _cover_download(self):
		rsp = requests.get(self.cover_find_url.format(self.manga_id))
		self.cover_art = json.loads(rsp.content)['results'][0]['data']['attributes']['fileName']

	def search(self, manga: List[str]) -> Tuple[str, str, str]:
		"""
			Look for a manga
			:param manga: the given string list that might represent a full manga (to be used as search token)
			:type manga: List[str]
			:return: A tuple with three values, the first being the id of the found manga, the second, the english
			name of it and the third one the cover art filename
			:rtype: Tuple[str, str]
		"""
		manga = '%20'.join(manga)
		url = f'{self.apiurl}/manga?title={manga}'
		rsp = requests.get(url).content
		self.manga_id = json.loads(rsp)['results'][0]['data']['id']
		self.manga_name = json.loads(rsp)['results'][0]['data']['attributes']['title']['en']
		self._cover_download()
		self.cover_art_file = self.cover_final_url.format(self.manga_id, self.cover_art)
		return self.manga_id, self.manga_name, self.cover_art_file

	def init(
			self,
			manga_name: str,
			manga_id: str,
			lang: Optional[str] = 'en',
			offset: Optional[int] = 0,
			chapter: Optional[str] = ''):
		"""
			Initial method if not given values on true __init__
			:param manga_name: this shall be used as foldername to download the chapters
			:type manga_name: Union[str, bytes, _PathLike[str], _PathLike[bytes]]
			:param manga_id: the uuid from the manga (obtainable through search method)
			:type manga_id: str
			:param lang: language of the manga (mostly will be 'en')
			:type lang: str
			:param chapter: the specific chapter i am looking for
			:type chapter: str
			:param offset: which chapter should the search begin from (not completely precise since mangas have bronken chapters as such: [10.2, 10.5, etc])
			:type offset: int
		"""
		self.manga_name = manga_name
		self.manga_id = manga_id
		self.full_url = f'{self.apiurl}/chapter?manga={self.manga_id}&limit=100&order[chapter]=asc&translatedLanguage[]={lang}&offset={offset}'
		self._save_response()
		self._save_chapters()
		# self._loop_through_chapters()
		return self.df

	def _write_pages(self, chapter: Dict):
		"""
			Writes the received chapters into the disk
			:param chapter: A pandas tuple that contains all the information there is to know about a single chapter from
			a manga, being the most important ones: chapter, data and hash
			:type chapter: Dict[Any, ...]
		"""
		count = 1
		for page in chapter.data:
			extension = page[-4:]
			file = f'{self.manga_name}\\{chapter.chapter:.1f}\\Page {count}{extension}'
			if not os.path.isfile(file):
				rsp = requests.get(self.final_url.format(chapter.hash, page))
				with open(file, 'wb') as f:
					f.write(rsp.content)
					print(f'Saved: <{file}>')
			else:
				print(f'{file} Exists')
			count += 1

	def _loop_through_chapters(self):
		for chapter in self.df.itertuples():
			self._make_folders(chapter_row=chapter)
			self._write_pages(chapter)

	def _save_chapters(self):
		"""
			Transforms the json object into a iterable object and then into a pandas DataFrame for better finding and
			positioning of all the chapters (it can be transformed into a csv for better human viewing but there's no
			computational need for that)
		"""

		column_names = ['id', 'type', 'chapter', 'language', 'hash', 'data']

		if self.json_chapters['results']:
			self.chapters = next(iter(self.json_chapters.values()))
			flattened_dict = pd.json_normalize(self.chapters, sep='.')
			full_dict = flattened_dict.to_dict(orient='records')
			self.df = pd.DataFrame(full_dict)
			self.df = self.df.drop('data.attributes.dataSaver', axis=1)
			self.df = self.df.drop('data.attributes.title', axis=1)
			self.df = self.df.drop('data.attributes.createdAt', axis=1)
			self.df = self.df.drop('data.attributes.version', axis=1)
			self.df = self.df.drop('data.attributes.updatedAt', axis=1)
			self.df = self.df.drop('data.attributes.publishAt', axis=1)
			self.df = self.df.drop('data.attributes.volume', axis=1)
			self.df = self.df.drop('relationships', axis=1)
			self.df = self.df.drop('result', axis=1)
			self.df['data.attributes.chapter'] = pd.to_numeric(
				self.df['data.attributes.chapter'], downcast='float')
			self.df.sort_values(by=['data.attributes.chapter'], inplace=True)

			self.df = self.df.rename(columns={self.df.columns[i]: column_names[i] for i in range(len(column_names))})

	def _save_response(self):
		"""
			Saves all the json reponse from the api into a json object
		"""
		manga = requests.get(self.full_url)
		self.json_chapters = json.loads(manga.text)

	def _make_folders(self, foldername: Optional[str] = 'cover', chapter_row=None):
		"""
			Makes all the needed folders: manga_name -> chapter_number
			:param foldername: name of a specific folder to be created
			:type foldername: str
			:param chapter_row: the chapter row containing all the needed data
			:type: Dict
		"""
		from re import sub
		self.manga_name = sub('[-!$%^&*()_+|~=`{}[]:";\'<>?,./]', '', self.manga_name)

		file = f'{self.manga_name}/{chapter_row.chapter:.1f}' if chapter_row else f'{self.manga_name}/{foldername}'
		if not os.path.exists(self.manga_name):
			os.mkdir(self.manga_name)
		if not os.path.exists(file):
			os.mkdir(file)
		return file


def setup(bot: commands.Bot):
	bot.add_cog(Manga(bot))
