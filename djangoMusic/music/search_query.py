from .fields import *
from .ISPager.dict_fetch_all import dict_fetch_all
from .track_query import track_query


def get_search_query(_get: dict, cur_fields_list: list[list[str, str, str, int | None]],
                     force: bool = False) -> dict | bool:
    """
    Формирование словаря с фрагментами SQL-запроса для объекта DjangoPager.
    Если не переданы параметры поиска и force == False, возвращается False.
    :param _get: Словарь GET-параметров.
    :param cur_fields_list: Список элементов HTML-формы, содержащих соответствующие имена полей в БД.
        Является результатом функции cur_fields.
    :param force: Флаг принуждения формирования запроса для вывода всех записей, когда страница «Поиск» запрашивается
        без поисковых параметров.
    :return: {'where': 'str', 'fields': 'str', 'tables': 'str', 'group': 'str', 'order': 'str'} | False
    """
    ff23 = fields()[23][2]  # track
    ff24 = fields()[24][2]  # author
    nro = 'IF(name_romaji IS NULL, name_original, name_romaji)'
    ft = ['InStr(', ', "', '") > 0', ' = "', '"']
    cf = []
    for i, f in enumerate(cur_fields_list):
        if i not in (0, 6):
            cf.append(f)
    nft = [
        [3, nro,		cf[0][2],  	ft[0] + cf[0][2] + ft[1], '', ft[2]],
        [0, cf[1][2],	ff23,   	ft[0] + cf[1][2] + ft[1], '', ft[2]],
        [0, cf[2][2],	ff23,   	ft[0] + cf[2][2] + ft[1], '', ft[2]],
        [0, cf[3][2],	ff23,   	ft[0] + cf[3][2] + ft[1], '', ft[2]],
        [1, nro,		cf[4][2],	cf[4][2] + ft[3], '', ft[4]],
        [0, cf[5][2],	ff23,   	cf[5][2] + ft[3], '', ft[4]],
        [3, nro,		cf[6][2],  	ft[0] + cf[6][2] + ft[1], '', ft[2]],
        [3, nro,		cf[7][2],  	ft[0] + cf[7][2] + ft[1], '', ft[2]],
        [3, nro,		cf[8][2],  	ft[0] + cf[8][2] + ft[1], '', ft[2]],
        [2, nro,		cf[9][2],	ft[0] + cf[9][2] + ft[1], '', ft[2]],
        [0, cf[10][2],	ff23,   	ft[0] + cf[10][2] + ft[1], '', ft[2]]
    ]
    al = 'AND' if 'chbStr' in _get else 'OR'
    result = {'where': ''}
    for i, f in enumerate(cf):
        if f[0] in _get and _get[f[0]]:
            if nft[i][0] == 0:
                nft[i][4] = _get.get(f[0])
            elif nft[i][0] == 1:
                query = f'SELECT {nft[i][1]} FROM {nft[i][2]} WHERE id = {_get.get(f[0])}'
                nft[i][4] = dict_fetch_all(query, True)[nft[i][1]]
            elif nft[i][0] > 1:
                query = f'SELECT {nft[i][1]} FROM {ff24 if nft[i][0] == 3 else nft[i][2]} WHERE id = '
                gl = _get.getlist(f[0])
                if isinstance(gl, list) and len(gl) > 1:
                    w = len(gl) - 1
                    for _id in gl:
                        query += _id + (' OR id = ' if w > 0 else '')
                        w -= 1
                else:
                    query += _get.get(f[0])
                nft[i][4] = dict_fetch_all(query)
            result['where'] += (f' {al} ' if result['where'] else '') + nft[i][3]
            if isinstance(nft[i][4], list):
                w = len(nft[i][4]) - 1
                for v in nft[i][4]:
                    result['where'] += v[nft[i][1]] + (f'{nft[i][5]} {al} {nft[i][3]}' if w > 0 else '')
                    w -= 1
            else:
                result['where'] += nft[i][4]
            result['where'] += nft[i][5]
    if not result['where'] and not force:
        return False
    result['where'] = 'WHERE ' + result['where'] if result['where'] else ''
    result['fields'] = '*'
    result['tables'] = track_query(cur_fields_list)
    result['group'] = ''
    result['order'] = 'ORDER BY '
    if 'sort' in _get and _get['sort']:
        result['order'] += find_field(_get['sort'][:5]) + (' DESC' if _get['sort'][5] == 'd' else '')
    elif 'sub' in _get and _get['sub'] == 'sort' and 'sel' in _get and _get['sel']:
        result['order'] += find_field(_get['sel']) + (' DESC' if 'chb' in _get else '')
        i = 1
        while f'sel{i}' in _get and _get[f'sel{i}']:
            result['order'] += ', ' + find_field(_get[f'sel{i}']) + (' DESC' if f'chb{i}' in _get else '')
            i += 1
    else:
        result['order'] += cur_fields_list[1][2] + ', ' + cur_fields_list[2][2]
    return result
