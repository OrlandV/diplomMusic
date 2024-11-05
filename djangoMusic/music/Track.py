from django.db import connection
from .track_query import track_query
from .ISPager.dict_fetch_all import dict_fetch_all
from .fields import *
from .Author import Author
from .Album import Album
from .OSTFrom import OSTFrom


class Track:
    def __init__(self, cf: list, tid: int):
        self.cf = cf
        self.id = tid
        item = self._get_items()
        self.performer = item[self.cf[1][2]]
        self.name_orig = item[self.cf[2][2]]
        self.name_rom = item[self.cf[3][2]]
        self.name_eng = item[self.cf[4][2]]
        self.album = item[self.cf[5][2]]
        self.number_in_album = item[self.cf[6][2]]
        self.duration = item[self.cf[7][2]]
        self.lyricist = item[self.cf[8][2]]
        self.composer = item[self.cf[9][2]]
        self.arranger = item[self.cf[10][2]]
        self.ost_from = item[self.cf[11][2]]
        self.notes = item[self.cf[12][2]]

    def _get_items(self) -> dict:
        query = f'''SELECT * FROM {track_query(self.cf)}
WHERE {self.cf[0][2]} = {self.id}'''
        return dict_fetch_all(query, True)

    def get_name(self, index: int) -> str | None:
        if index == 2:
            return self.name_orig
        elif index == 3:
            return self.name_rom
        elif index == 4:
            return self.name_eng
        else:
            return None

    def get_author_id(self, index: int) -> tuple:
        a = fields()[24][2]
        _id = self.cf[0][2]
        ai = self.cf[index][2]
        t = fields()[23][2]
        query = f'''SELECT {a}_{_id}
FROM {ai}
WHERE {ai}.{t}_{_id} = {self.id}'''
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_author(self, index: int, is_dict: bool = False, _get: dict | None = None) -> str | dict | None:
        if is_dict:
            res = {}
            for _id in self.get_author_id(index):
                res[_id[0]] = ''
                author = Author(cur_fields([0, 21, 22]), 2, _get, index=index)
                af = author.get_all(False)
                for i, f in enumerate(af):
                    res[_id[0]] += f + (' / ' if i < len(af) - 1 else '')
                return res
        elif index == 1:
            return self.performer
        elif index == 8:
            return self.lyricist
        elif index == 9:
            return self.composer
        elif index == 10:
            return self.arranger
        else:
            return None

    def get_album_id(self) -> tuple:
        query = f'''SELECT {self.cf[5][2]}
FROM {fields()[23][2]}
WHERE {self.cf[0][2]} = {self.id}'''
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_album(self, is_dict: bool = False, cf: list | None = None) -> str | dict:
        if is_dict:
            res = {}
            for _id in self.get_album_id():
                res[_id[0]] = ''
                album = Album(cf, 2)
                af = album.get_all()
                for i, f in enumerate(af):
                    res[_id[0]] += f + (' / ' if i < len(af) - 1 else '')
            return res
        else:
            return self.album

    def get_ost_from_id(self) -> tuple:
        o = self.cf[11][2]
        _id = self.cf[0][2]
        t = fields()[23][2]
        query = f'''SELECT {o}_{_id}
FROM {t}_{o}
WHERE {t}_{_id} = {self.id}'''
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_ost_from(self, is_dict: bool = False, cf: list | None = None) -> str | dict:
        if is_dict:
            res = {}
            for _id in self.get_ost_from_id():
                res[_id[0]] = ''
                ost = OSTFrom(cf)
                of = ost.get_all()
                for i, f in enumerate(of):
                    res[_id[0]] += f + (' / ' if i < len(of) - 1 else '')
            return res
        else:
            return self.ost_from

    def get_all(self, is_dict: bool = False, album_fields: list | None = None, ost_fields: list | None = None,
                _get: dict | None = None) -> list:
        return [
            self.id,
            self.get_author(1, is_dict, _get),
            self.name_orig,
            self.name_rom,
            self.name_eng,
            self.get_album(is_dict, album_fields),
            self.number_in_album,
            self.duration,
            self.get_author(8, is_dict, _get),
            self.get_author(9, is_dict, _get),
            self.get_author(10, is_dict, _get),
            self.get_ost_from(is_dict, ost_fields),
            self.notes
        ]
