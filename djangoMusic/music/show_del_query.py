from .fields import *
from .track_query import track_query
from .album_query import get_album_query


def get_show_del_query(fni: int, cf: list, _id: int, rel: int = 0) -> dict:
    result = {
        'fields': '*',
        'where': '',
        'group': '',
        'order': ''
    }
    if fni == 5:
        result['tables'] = track_query(
            cf, 1, fni, f'WHERE {fields()[23][2]}.{fields()[fni][2]} = {_id}'
        )
    elif fni == 11:
        result['tables'] = track_query(
            cf, 1, fni, f'WHERE {fields()[23][2]}_{fields()[fni][2]}.{fields()[fni][2]}_{fields()[0][2]} = {_id}'
        )
    elif fni in (17, 18, 19):
        result['tables'] = get_album_query(
            cf, 1, rel=fni, where=f'WHERE {fields()[5][2]}.{fields()[fni][2]} = {_id}'
        )
    elif fni == 24:
        result['tables'] = track_query(
            cf, 1, rel, f'WHERE {fields()[rel][2]}.{fields()[24][2]}_{fields()[0][2]} = {_id}'
        )
    return result
