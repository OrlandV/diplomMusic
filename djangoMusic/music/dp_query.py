"""
Формирование словаря с фрагментами SQL-запроса для объекта DjangoPager.
"""
from .fields import fields, find_field
from .album_query import get_album_query
from .author_query import get_author_query
from .track_query import track_query


def get_dp_query(cf: list, _get: dict, table: str) -> dict:
    """
    Формирование словаря с фрагментами SQL-запроса для объекта DjangoPager.
    :param cf: Список элементов HTML-формы, содержащих соответствующие имена полей в БД.
        Является результатом функции cur_fields.
    :param _get: Словарь GET-параметров.
    :param table: Имя таблицы БД.
    :return: {'where': 'str', 'fields': 'str', 'tables': 'str', 'group': 'str', 'order': 'str'}
    """
    result = {
        'fields': '*',
        'where': '',
        'group': '',
        'order': 'ORDER BY '
    }
    if 'sort' in _get and _get['sort']:
        sort = _get.get('sort')
        result['order'] += find_field(sort[:5]) + (' DESC' if sort[5] == 'd' else '')
    elif 'sub' in _get and _get['sub'] == 'sort' and 'sel' in _get and _get['sel']:
        result['order'] += find_field(_get.get('sel')) + (' DESC' if 'chb' in _get else '')
        i = 1
        while f'sel{i}' in _get and _get[f'sel{i}']:
            result['order'] += ', ' + find_field(_get[f'sel{i}']) + (' DESC' if f'chb{i}' in _get else '')
            i += 1
    else:
        if table == fields()[5][2]:
            result['tables'] = get_album_query(cf, 1)
            result['order'] += f'{cf[1][2]}, {cf[2][2]}'
        elif table == fields()[11][2]:
            result['tables'] = table
            result['order'] += f'{cf[1][2]}, {cf[2][2]}'
        elif table == fields()[23][2]:
            result['tables'] = track_query(cf)
            result['order'] += f'{cf[1][2]}, {cf[2][2]}, {cf[5][2]}, {cf[6][2]}'
        elif table == fields()[24][2]:
            result['tables'] = get_author_query(cf, 1)
            result['order'] += cf[2][2]
        elif table in (fields()[17][2], fields()[18][2], fields()[19][2]):
            result['tables'] = table
            result['order'] += cf[1][2]
    return result
