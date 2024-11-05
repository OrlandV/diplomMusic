from .fields import *


def get_show_ost_from_query(f: list, _get) -> dict:
    result = {
        'fields': '*',
        'tables': fields()[11][2],
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
        result['order'] += f'{f[1][2]}, {f[2][2]}'
    return result
