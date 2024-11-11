from .author_query import get_author_query
from .ISPager.dict_fetch_all import dict_fetch_all


class Author:
    """
    Класс Автор для упрощения подстановки данных в форму правки или вывода полного представления при удалении.
    :param cf: Список полей — результат функции cur_fields.
    :param mode: Номер или имя режима запроса в функции get_author_query.
    :param _get: Словарь GET-параметров.
    :param aid: ID автора.
    :param index: Индекс в списке (функции) fields соответствующей роли автора
        (вокалист | поэт | композитор | аранжировщик).
    """
    def __init__(self, cf: list, mode: int | str, _get: dict | None = None, aid: int | bool = False, index: int = 1):
        item = self.__get_items(cf, mode, _get, aid, index)
        self.id = aid or item[cf[0][2]]
        self.name_orig = item[cf[1][2]]
        self.name_rom = item[cf[2][2]]

    @staticmethod
    def __get_items(cf: list, mode: int | str, _get: dict | None = None, aid: int | bool = False,
                   index: int = 1) -> dict:
        query = 'SELECT ' + get_author_query(cf, mode, _get, False, index)
        query += f'\nWHERE {cf[0][2]} = {aid}' if aid else ''
        return dict_fetch_all(query, True)

    def get_name(self, number: int = 0) -> str:
        if number == 1:
            return self.name_orig
        elif number == 2:
            return self.name_rom

    def get_all(self, aid: bool = True) -> list:
        res = [self.id] if aid else []
        for i in (1, 2):
            res.append(self.get_name(i))
        return res
