from .fields import *
from .ISPager.dict_fetch_all import dict_fetch_all


class OSTFrom:
    def __init__(self, cf: list, oid: int | bool = False):
        item = self._get_items(cf, oid)
        self.id = oid or item[cf[0][2]]
        self.name_orig = item[cf[1][2]]
        self.name_rom = item[cf[2][2]]
        self.name_eng = item[cf[3][2]]
        self.date = item[cf[4][2]]

    @staticmethod
    def _get_items(cf: list, oid: int | bool = False) -> dict:
        query = f'''SELECT {cf[0][2]}, {cf[1][2]}, {cf[2][2]}, {cf[3][2]}, {cf[4][2]}
FROM {fields()[11][2]}''' + (f'\nWHERE {cf[0][2]} = {oid}' if oid else '')
        return dict_fetch_all(query, True)

    def get_name(self, index: int) -> str | None:
        if index == 1:
            return self.name_orig
        elif index == 2:
            return self.name_rom
        elif index == 3:
            return self.name_eng
        else:
            return None

    def get_all(self) -> list:
        return [
            self.id,
            self.name_orig,
            self.name_rom,
            self.name_eng,
            self.date
        ]
