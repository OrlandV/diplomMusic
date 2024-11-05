from .fields import fields
from .ISPager.dict_fetch_all import dict_fetch_all


class Name:
    def __init__(self, cf: list, index: int = 1, nid: int | bool = False):
        item = self._get_items(cf, index, nid)
        self.id = nid or item[cf[0][2]]
        self.name = item[cf[1][2]]

    @staticmethod
    def _get_items(cf: list, index: int = 1, nid: int | bool = False) -> dict:
        query = f'''SELECT {cf[0][2]}, {cf[1][2]}
FROM {fields()[index][2]}''' + (f'''
WHERE {cf[0][2]} = {nid}''' if nid else '')
        return dict_fetch_all(query, True)

    def get_all(self) -> list:
        return [self.id, self.name]