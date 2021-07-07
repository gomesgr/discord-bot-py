import os
from logging import getLogger
from typing import Optional, List, Dict, Tuple, Union
import requests
import json

import handler
import bot_constants
import pandas as pd
from discord.ext import commands, tasks
from discord import TextChannel, Embed, PermissionOverwrite, utils, File
import shutil

logger = getLogger('manga')
# pd.options.display.float_format = '{:.1f}'.format

JSON_CHANNEL_IDS_FILE = 'text_channels.json'


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
		self.users_using: Dict[str, int] = {}
		self.items = 5

		self.messages_to_delete: List[str] = []

	@tasks.loop(seconds=5.0)
	async def delete_messages(self):
		if self.messages_to_delete:
			await handler.delete_message(self.messages_to_delete.pop(), logger)

	@commands.Cog.listener()
	async def on_ready(self):
		message = 'Cog Manga ready'
		print(message)
		logger.info(message)
		self.delete_messages.start()

	@commands.command(name=bot_constants.MANGA_SEARCH, aliases=bot_constants.MANGA_SEARCH_ALIASES)
	async def mangasearch(self, ctx: commands.Context, *manga_name: str):
		self.count = 0
		manga_name = list(manga_name)
		self.manga['uuid'], self.manga['name'], self.manga['cover_url'] = self.md.search(
			manga_name)
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

	async def _send_chapters(self, reaction, chapter_number):
		self.md.init(self.manga['name'], self.manga['uuid'], chapter=chapter_number, download=True)
		print(self.md.saved_chapters)
		for file in self.md.saved_chapters:
			print(file)
			with open(file, 'rb') as f:
				chapter = File(f)
				await reaction.message.channel.send(file=chapter)
		self.md.saved_chapters.clear()

	def _reactions(self, reaction) -> str:
		embed = reaction.message.embeds[0]

		def one():
			return embed.to_dict()['fields'][0]

		def two():
			return embed.to_dict()['fields'][1]

		def three():
			return embed.to_dict()['fields'][2]

		def four():
			return embed.to_dict()['fields'][3]

		def five():
			return embed.to_dict()['fields'][4]

		funs = {
			bot_constants.NUMBERS_ONE_TO_FIVE[0]: one,
			bot_constants.NUMBERS_ONE_TO_FIVE[1]: two,
			bot_constants.NUMBERS_ONE_TO_FIVE[2]: three,
			bot_constants.NUMBERS_ONE_TO_FIVE[3]: four,
			bot_constants.NUMBERS_ONE_TO_FIVE[4]: five,
		}
		v = funs[reaction.emoji]()
		# self.manga_df.loc[self.manga_df['chapter'] == v['value']]
		return v['value']

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if user.bot:
			return

		channels = handler.load_json(JSON_CHANNEL_IDS_FILE)

		# reaction.message.id == channels[str(reaction.message.guild)][str(user.id)]

		if self.msg_embed_cover_id == reaction.message.id and reaction.emoji == bot_constants.RIGHT_WRONG[0]:
			# self.count = 1
			try:
				assert(channels[str(reaction.message.guild.id)][str(user.id)])
				msg = await handler.send_message(self.ctx, logger, content='Canal Criado')
				self.messages_to_delete.append(msg)
				print(self.messages_to_delete)
				return
			except KeyError:
				await self._init_search()
				return

		if str(reaction.message.channel.id) == channels[str(reaction.message.guild.id)][str(user.id)]:
			embed = Embed()

			# CLOSE
			if reaction.emoji == bot_constants.RIGHT_WRONG[1]:
				tc_delete = self.bot.get_channel(int(channels[str(reaction.message.guild.id)][str(user.id)]))
				await tc_delete.delete()
				del channels[str(reaction.message.guild.id)][str(user.id)]
				self.md.saved_chapters.clear()
				shutil.rmtree(self.md.manga_name)

				handler.dump_json(JSON_CHANNEL_IDS_FILE, channels)
				return

			elif reaction.emoji in bot_constants.NUMBERS_ONE_TO_FIVE:
				chapter = self._reactions(reaction)
				await self._send_chapters(reaction, chapter)
				return

			# NEXT
			elif reaction.emoji == bot_constants.NEXT:
				embed.title = 'Escolha o capitulo abaixo:'
				self.manga_page += 1
				self.items += 5

			# PREVIOUS
			elif reaction.emoji == bot_constants.PREVIOUS and self.manga_page >= 1:
				embed.title = 'Escolha o capitulo abaixo:'
				self.manga_page -= 1
				self.items -= 5

			# LAST
			elif reaction.emoji == bot_constants.LAST:
				self.manga_page = 20
				self.items = 100

			# FIRST
			elif reaction.emoji == bot_constants.FIRST:
				self.manga_page = 0
				self.items = 5

			for count, x in enumerate(self.manga_df.iloc[self.items - 5:self.items].itertuples()):
				embed.add_field(
					name=bot_constants.NUMBERS_ONE_TO_FIVE[count],
					value=x.chapter,
					inline=False)

			await reaction.message.edit(embed=embed)

	async def _init_search(self):
		"""
			Starts iteration over manga chapters, creates text channel and adds reactions to message on it
		"""
		self.manga_df = self.md.init(
			self.manga['name'], self.manga['uuid'])
		created_channel = await self._create_text_channel()
		embed = Embed()
		embed.title = 'Escolha o capitulo abaixo:'

		first_five = [
			x.chapter for x in self.manga_df.head().itertuples()]

		for i in range(5):
			embed.add_field(
				name=bot_constants.NUMBERS_ONE_TO_FIVE[i],
				value=first_five[i],
				inline=False)

		message = await created_channel.send(embed=embed)
		await message.add_reaction(bot_constants.FIRST)
		await message.add_reaction(bot_constants.PREVIOUS)
		await message.add_reaction(bot_constants.NEXT)
		await message.add_reaction(bot_constants.LAST)
		[await message.add_reaction(v) for v in bot_constants.NUMBERS_ONE_TO_FIVE]
		await message.add_reaction(bot_constants.RIGHT_WRONG[1])

	async def _change_context(self, channel):
		pass

	async def _create_text_channel(self):
		"""
				Creates the user-related text-channel
		"""

		channels = handler.load_json(JSON_CHANNEL_IDS_FILE)

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

		handler.dump_json(JSON_CHANNEL_IDS_FILE, channels)

		return channel


class Mangadownloader:
	"""
			Downloads given manga chapters using maximum quality (data) from mangadex api. (limited to 100 chapters)
	"""

	def __init__(self):
		self.saved_chapters: List[str] = []

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
		self.cover_art = json.loads(
			rsp.content)['results'][0]['data']['attributes']['fileName']

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
		self.manga_name = json.loads(
			rsp)['results'][0]['data']['attributes']['title']['en']
		self._cover_download()
		self.cover_art_file = self.cover_final_url.format(
			self.manga_id, self.cover_art)
		return self.manga_id, self.manga_name, self.cover_art_file

	def init(
			self,
			manga_name: str,
			manga_id: str,
			lang: Optional[str] = 'en',
			offset: Optional[int] = 0,
			chapter: Optional[str] = '',
			download: Optional[bool] = False):
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
				:param download: boolean to tell if i want to download the chapters or not
				:type download: bool
		"""
		self.manga_name = manga_name
		self.manga_id = manga_id
		if not chapter:
			self.full_url = f'{self.apiurl}/chapter?manga={self.manga_id}&limit=100&order[chapter]=asc&translatedLanguage[]={lang}&offset={offset}'
		else:
			self.full_url = f'{self.apiurl}/chapter?manga={self.manga_id}&translatedLanguage[]={lang}&chapter={chapter}'
		self._save_response()
		self._save_chapters()
		print(self.full_url)
		if download:
			self._loop_through_chapters()
		return self.df

	def _write_pages(self, chapter: Dict):
		"""
				Writes the received chapters into the disk
				:param chapter: A pandas tuple that contains all the information there is to know about a single chapter from
				a manga, being the most important ones: chapter, data and hash
				:type chapter: Dict[Any, ...]
		"""
		for count, page in enumerate(chapter.data):
			extension = page[-4:]
			file = f'{self.manga_name}\\{chapter.chapter}\\Page {count}{extension}'
			self.saved_chapters.append(file)
			if not os.path.isfile(file):
				rsp = requests.get(self.final_url.format(chapter.hash, page))
				with open(file, 'wb') as f:
					f.write(rsp.content)
					print(f'Saved: <{file}>')
			else:
				print(f'{file} Exists')

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

		if not self.json_chapters['results']:
			return
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

		self.df['data.attributes.chapter'] = pd.to_numeric(self.df['data.attributes.chapter'], downcast='float')
		self.df.sort_values(by=['data.attributes.chapter'], inplace=True)

		column_names = [
			'id',
			'type',
			'chapter',
			'language',
			'hash',
			'data']

		self.df = self.df.rename(
			columns={
				self.df.columns[i]: column_names[i] for i in range(
					len(column_names))})

		self.df['chapter'] = self.df['chapter'].astype(str)

		for i in range(len(self.df['chapter'])):
			spl = self.df['chapter'][i].split('.')
			if len(spl[0]) < 2:
				self.df['chapter'][i] = self.df['chapter'][i][0:3]
			elif len(spl[0]) < 3:
				self.df['chapter'][i] = self.df['chapter'][i][0:4]
			elif len(spl[0]) < 4:
				self.df['chapter'][i] = self.df['chapter'][i][0:5]

			if self.df['chapter'][i][-1] == '0':
				self.df['chapter'][i] = self.df['chapter'][i][:-2]

	def _save_response(self):
		"""
				Saves all the json reponse from the api into a json object
		"""
		manga = requests.get(self.full_url)
		self.json_chapters = json.loads(manga.text)

	def _make_folders(
			self,
			foldername: Optional[str] = 'cover',
			chapter_row=None):
		"""
				Makes all the needed folders: manga_name -> chapter_number
				:param foldername: name of a specific folder to be created
				:type foldername: str
				:param chapter_row: the chapter row containing all the needed data
				:type: Dict
		"""
		from re import sub
		self.manga_name = sub(
			r'[^\w]',
			'',
			self.manga_name)

		file = f'{self.manga_name}/{chapter_row.chapter}' if chapter_row else f'{self.manga_name}/{foldername}'
		if not os.path.exists(self.manga_name):
			os.mkdir(self.manga_name)
		if not os.path.exists(file):
			os.mkdir(file)
		return file


def setup(bot: commands.Bot):
	bot.add_cog(Manga(bot))
