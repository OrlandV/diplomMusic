from django.db import connection
from .fields import fields


def execute(query: str, func: str | None = None):
    with connection.cursor() as cursor:
        cursor.execute(query)
        if func == 'fetchone':
            return cursor.fetchone()[0]


def relationships(fni: int, _id: int) -> list:
    cnt = []
    if fni == 5:
        if execute(f'SELECT COUNT(*) FROM {fields()[23][2]} WHERE {fields()[fni][2]} = {_id}',
                   'fetchone'):
            cnt.append(fni)
    elif fni == 11:
        if execute(f'SELECT COUNT(*) FROM {fields()[23][2]}_{fields()[fni][2]} '
                   f'WHERE {fields()[fni][2]}_{fields()[0][2]} = {_id}', 'fetchone'):
            cnt.append(fni)
    elif fni in (17, 18, 19):
        if execute(f'SELECT COUNT(*) FROM {fields()[5][2]} WHERE {fields()[fni][2]} = {_id}',
                   'fetchone'):
            cnt.append(fni)
    elif fni == 24:
        for i in (1, 8, 9, 10):
            if execute(f'SELECT COUNT(*) FROM {fields()[i][2]} WHERE {fields()[24][2]}_{fields()[0][2]} = {_id}',
                       'fetchone'):
                cnt.append(i)
    return cnt


def del_(fni: int, _id: int):
    df = 'DELETE FROM '
    w = ' WHERE '
    if fni == 11:
        execute(f'{df}{fields()[23][2]}_{fields()[fni][2]}{w}{fields()[fni][2]}_{fields()[0][2]} = {_id}')
        return
    elif fni in (23, 24):
        for i in (1, 8, 9, 10, 11):
            if i == 11 and fni == 24:
                break
            t = fields()[i][2] if i < 11 else f'{fields()[23][2]}_{fields()[11][2]}'
            execute(f'{df}{t}{w}{fields()[fni][2]}_{fields()[0][2]} = {_id}')
    execute(f'{df}{fields()[fni][2]}{w}{fields()[0][2]} = {_id}')
