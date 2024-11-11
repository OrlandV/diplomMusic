"""
Пагинатор, использующий django.db.connection для подключения к базе данных.
"""
from django.db import connection
from .Pager import Pager
from .dict_fetch_all import dict_fetch_all


class DjangoPager(Pager):
    """
    Пагинатор, использующий django.db.connection для подключения к базе данных.
    :param view: Объект представления.
    :param table_name: Таблица базы данных (либо подзапрос).
    :param fields: Имена полей (столбцов) в выборке.
    :param where: WHERE-условие SQL-запроса.
    :param group: Группировка выборки.
    :param order: Сортировка выборки.
    :param items_per_page: Количество элементов на странице.
    :param links_count: Количество видимых ссылок слева и справа от текущей страницы.
    :param get_params: Дополнительные параметры, которые необходимо передавать по ссылкам.
    :param counter_param: Название GET-параметра, через который передаётся номер текущей страницы.
    """
    def __init__(self, view, table_name: str, fields: str = '*', where: str = '', group: str = '', order: str = '',
                 items_per_page: int = 10, links_count: int = 3, get_params: str | None = None,
                 counter_param: str = 'page'):
        super().__init__(view, items_per_page, links_count, get_params, counter_param)
        self.table_name = table_name
        self.fields = fields
        self.where = where
        self.group = group
        self.order = order

    def getItemsCount(self) -> int:
        """
        Количество элементов (строк).
        """
        query = f'''SELECT COUNT(*) AS total
FROM {self.table_name}
{self.where}
{self.group}'''
        return dict_fetch_all(query, True)['total']

    def getItems(self, _get: dict) -> tuple[tuple] | int:
        """
        Элементы выборки для текущей страницы.
        Кортеж элементов (строк), представленных кортежами полей.
        Если элементов нет, то возвращается 0, эквивалентный False.
        :param _get: Словарь (либо QueryDict) request.GET.
        """
        current_page = self.getCurrentPage(_get)
        total_pages = self.getPagesCount()
        if current_page <= 0 or current_page > total_pages:
            return 0
        first = (current_page - 1) * self.getItemsPerPage()
        query = f'''SELECT {self.fields}
FROM {self.table_name}
{self.where}
{self.group}
{self.order}
LIMIT {first}, {self.getItemsPerPage()}'''
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
