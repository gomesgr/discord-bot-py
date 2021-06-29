import os
from logging import getLogger
from typing import Optional, List, Dict, Tuple, Any, Union
import requests
import json

import bot_constants
import pandas as pd
from discord.ext import commands

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
        uuid, name = md.search(manga_name)
        print(uuid, name)


class Mangadownloader:
    def __init__(self):
        self.manga_name: Optional[str] = ''
        self.manga_id: Optional[str] = ''
        self.apiurl = 'https://api.mangadex.org'
        self.json_chapters: Dict[str] = {}
        self.chapters: List[str] = []
        self.final_url = 'https://uploads.mangadex.org/data/{0}/{1}'
        self.full_url: Optional[str] = ''
        self.df: Optional[pd.DataFrame] = None

    def search(self, manga: List[str]) -> Tuple[str, str]:
        """
                :param manga: the given list of strings that might represent a full manga (to be used as search token)
                :type manga: List[str]
                :return: A tuple with two values, the first being the id of the found manga and the second, the english
                name of it
                :rtype: Tuple[str, str]
        """
        manga = '%20'.join(manga)  # %20 represents an empty space
        url = f'{self.apiurl}/manga?title={manga}'
        print(url)
        rsp = requests.get(url).content
        return json.loads(rsp)['results'][0]['data']['id'], json.loads(rsp)[
            'results'][0]['data']['attributes']['title']['en']

    def init(
            self,
            manga_name: Union[str, Any],
            manga_id: Optional[str] = '',
            lang: Optional[str] = 'en',
            chapter: Optional[str] = '',
            offset: Optional[int] = 0,
            save_file: Optional[bool] = False):
        self.manga_name = manga_name
        self.manga_id = manga_id
        if chapter:
            self.full_url = f'{self.apiurl}/chapter?manga={self.manga_id}&limit=100&order[chapter]=asc&translatedLanguage[]={lang}&offset={offset}&chapter={chapter}'
        else:
            self.full_url = f'{self.apiurl}/chapter?manga={self.manga_id}&limit=100&order[chapter]=asc&translatedLanguage[]={lang}&offset={offset}'
        self._save_response()
        self._save_chapters(save_file)
        # self._loop_through_chapters()

    def _write_pages(self, chapter: Dict):
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
            self._make_folders(chapter)
            self._write_pages(chapter)

    def _save_chapters(self, save: Optional[bool] = False):

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
            logger.info(self.df.head())
            if save:
                path = f'{self.manga_name}.xlsx'
                w = pd.ExcelWriter(path)
                self.df.to_excel(w)
                w.save()
                logger.info(f'Dataframe copy saved into: <{path}>')

    def _save_response(self):
        print(self.full_url)
        manga = requests.get(self.full_url)
        self.json_chapters = json.loads(manga.text)
        # print(self.json_chapters)

    def _delete_folder(self):
        from shutil import rmtree
        rmtree(self.manga_name, ignore_errors=True)
        return True

    def _make_folders(self, chapter_row: Dict):
        if not os.path.exists(self.manga_name):
            os.mkdir(self.manga_name)
        file = f'{self.manga_name}/{chapter_row.chapter:.1f}'
        if not os.path.exists(file):
            os.mkdir(file)


def setup(bot: commands.Bot):
    bot.add_cog(Manga(bot))
