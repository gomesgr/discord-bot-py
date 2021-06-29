import os
from logging import getLogger
from typing import Optional, List, Dict, Tuple, Any, Union
import requests
import json

import handler
import bot_constants
import pandas as pd
from discord.ext import commands
from discord import Embed

logger = getLogger('discord')


class Manga(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        message = 'Cog Manga ready'
        print(message)
        logger.info(message)

    @commands.command(name=bot_constants.MANGA_SEARCH,
                      aliases=bot_constants.MANGA_SEARCH_ALIASES)
    async def mangasearch(self, ctx: commands.Context, *manga_name: str):
        manga_name = list(manga_name)
        md = Mangadownloader()
        uuid, name, cover = md.search(manga_name)
        embed = Embed()
        print(cover)
        embed.set_image(url=cover)
        embed.title = 'Capa'
        embed.set_footer(text=name)
        embed.description = 'É esse o mangá que você está procurando?'
        msg = await handler.send_message(ctx, logger, embed=embed, emojis=True)
        msgid = msg.id
        [await handler.add_reaction(msg, reaction) for reaction in bot_constants.RIGHT_WRONG]


class Mangadownloader:
    """
        Downloads given manga chapters using maximum quality (data) from mangadex api. (limited to 100 chapters)
    """

    def __init__(self):
        self.manga_name: Optional[str] = ''
        self.manga_id: Optional[str] = ''

        self.json_chapters: Dict[str] = {}
        self.df: Optional[pd.DataFrame] = None
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
        self.cover_art = json.loads(rsp.content)[
            'results'][0]['data']['attributes']['fileName']

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
        self.cover_art_file = self.cover_final_url.format(self.manga_id, self.cover_art)
        return self.manga_id, self.manga_name, self.cover_art_file

    def init(
            self,
            manga_name: Union[str, Any],
            manga_id: Optional[str] = '',
            lang: Optional[str] = 'en',
            chapter: Optional[str] = '',
            offset: Optional[int] = 0,
            save_file: Optional[bool] = False):
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
            :param save_file: A boolean optional value to tell if you want to save onto a .xlsx file or not (standard being False)
            :type save_file: Optional[bool]
        """
        self.manga_name = manga_name
        self.manga_id = manga_id
        if chapter:
            self.full_url = f'{self.apiurl}/chapter?manga={self.manga_id}&limit=100&order[chapter]=asc&translatedLanguage[]={lang}&offset={offset}&chapter={chapter}'
        else:
            self.full_url = f'{self.apiurl}/chapter?manga={self.manga_id}&limit=100&order[chapter]=asc&translatedLanguage[]={lang}&offset={offset}'
        # self._save_response()
        # self._save_chapters(save_file)
        # self._loop_through_chapters()

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

    def _save_chapters(self, save: Optional[bool] = False):
        """
            Transforms the json object into a iterable object and then into a pandas DataFrame for better finding and
            positioning of all the chapters (it can be transformed into a csv for better human viewing but there's no
            computational need for that)
            :param save: A boolean optional value to tell if you want to save onto a .xlsx file or not (standard being False)
            :type save: bool
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

            self.df = self.df.rename(
                columns={
                    self.df.columns[i]: column_names[i] for i in range(
                        len(column_names))})
            # print(self.df.head())
            # if save:
            #     path = f'{self.manga_name}.xlsx'
            #     w = pd.ExcelWriter(path)
            #     self.df.to_excel(w)
            #     w.save()
            #     print(f'Dataframe copy saved into: <{path}>')

    def _save_response(self):
        """
            Saves all the json reponse from the api into a json object
        """
        manga = requests.get(self.full_url)
        self.json_chapters = json.loads(manga.text)

    def _make_folders(self, foldername: Optional[str] = 'cover', chapter_row: Optional[Dict] = dict()):
        """
            Makes all the needed folders: manga_name -> chapter_number
            :param foldername: name of a specific folder to be created
            :type foldername: str
            :param chapter_row: the chapter row containing all the needed data
            :type: Dict
        """
        file = f'{self.manga_name}/{chapter_row.chapter:.1f}' if chapter_row else f'{self.manga_name}/{foldername}'

        if not os.path.exists(self.manga_name):
            os.mkdir(self.manga_name)
        if not os.path.exists(file):
            os.mkdir(file)
        return file


def setup(bot: commands.Bot):
    bot.add_cog(Manga(bot))
