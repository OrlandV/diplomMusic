from django.db import connection
from .Pager import Pager
from .dict_fetch_all import dict_fetch_all


class DjangoPager(Pager):
    def __init__(self, view, table_name: str, fields: str = '*', where: str = '', params: list = [], group: str = '',
                 order: str = '', items_per_page: int = 10, links_count: int = 3, get_params: str | None = None,
                 counter_param: str = 'page'):
        super().__init__(view, items_per_page, links_count, get_params, counter_param)
        self.table_name = table_name
        self.fields = fields
        self.where = where
        self.params = params
        self.group = group
        self.order = order

    def getItemsCount(self) -> int:
        query = f'''SELECT COUNT(*) AS total
FROM {self.table_name}
{self.where}
{self.group}'''
        return dict_fetch_all(query, True)['total']

    def getItems(self, _get) -> tuple[tuple] | int:
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
