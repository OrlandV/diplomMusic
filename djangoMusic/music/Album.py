from .album_query import get_album_query
from .ISPager.dict_fetch_all import dict_fetch_all


class Album:
    """
    Класс Альбом для упрощения подстановки данных в форму правки или вывода полного представления при удалении.
    :param cf: Список полей — результат функции cur_fields.
    :param mode: Номер или имя режима запроса в функции get_album_query.
    :param aid: ID альбома.
    """
    def __init__(self, cf: list, mode: int | str, aid: int | bool = False):
        item = self.__get_items(cf, mode, aid)
        self.id = aid or item[cf[0][2]]
        self.date = item[cf[1][2]]
        self.catalog_number = item[cf[2][2]]
        self.name_orig = item[cf[3][2]]
        self.name_rom = item[cf[4][2]]
        self.name_eng = item[cf[5][2]]
        self.count_of_discs = item[cf[6][2]]
        self.count_of_tracks = item[cf[7][2]]
        self.media_format = item[cf[8][2]]
        self.label = item[cf[9][2]]
        self.manufacturer = item[cf[10][2]]
        self.note = item[cf[11][2]]

    @staticmethod
    def __get_items(cf: list, mode: int | str, aid: int | bool = False) -> dict:
        query = get_album_query(cf, mode, aid)
        return dict_fetch_all(query, True)

    def get_name(self, index: int) -> str | None:
        if index == 3:
            return self.name_orig
        elif index == 4:
            return self.name_rom
        elif index == 5:
            return self.name_eng
        else:
            return None

    def get_all(self) -> list:
        return [
            self.id,
            self.date,
            self.catalog_number,
            self.name_orig,
            self.name_rom,
            self.name_eng,
            self.count_of_discs,
            self.count_of_tracks,
            self.media_format,
            self.label,
            self.manufacturer,
            self.note
        ]
