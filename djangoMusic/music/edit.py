"""
Модуль с функциями, выполняющими непосредственное обновление записей в базе данных.
"""
from django.db import connection
from re import escape
from .fields import fields


def edit_name(index: int, f: list, _post, _id: int):
    query = f'''UPDATE {fields()[index][2]} SET
    {f[1][2]} = "{escape(_post[f[1][0]])}"
WHERE {f[0][2]} = {_id}'''
    with connection.cursor() as cursor:
        cursor.execute(query)


def edit_author(f: list, _post, _id: int):
    query = f'''UPDATE {fields()[24][2]} SET
    {f[1][2]} = "{escape(_post[f[1][0]])}",
    {f[2][2]} = ''' + (f'"{escape(_post[f[2][0]])}"' if f[2][0] in _post and _post[f[2][0]] else 'NULL') + f'''
WHERE {f[0][2]} = {_id}'''
    with connection.cursor() as cursor:
        cursor.execute(query)


def edit_ost_from(f: list, _post, _id: int):
    query = f'''UPDATE {fields()[11][2]} SET
    {f[1][2]} = "{escape(_post[f[1][0]])}",
    {f[2][2]} = ''' + (f'"{escape(_post[f[2][0]])}"' if f[2][0] in _post and _post[f[2][0]] else 'NULL') + f''',
    {f[3][2]} = ''' + (f'"{escape(_post[f[3][0]])}"' if f[3][0] in _post and _post[f[3][0]] else 'NULL') + f''',
    {f[4][2]} = "{_post[f[4][0]]}"
WHERE {f[0][2]} = {_id}'''
    with connection.cursor() as cursor:
        cursor.execute(query)


def edit_album(f: list, _post, _id: int):
    query = f'''UPDATE {fields()[5][2]} SET
    {f[1][2]} = "{_post[f[1][0]]}",
    {f[2][2]} = ''' + (f'"{escape(_post[f[2][0]])}"' if f[2][0] in _post and _post[f[2][0]] else 'NULL') + f''',
    {f[3][2]} = "{escape(_post[f[3][0]])}",
    {f[4][2]} = ''' + (f'"{escape(_post[f[4][0]])}"' if f[4][0] in _post and _post[f[4][0]] else 'NULL') + f''',
    {f[5][2]} = ''' + (f'"{escape(_post[f[5][0]])}"' if f[5][0] in _post and _post[f[5][0]] else 'NULL') + f''',
    {f[6][2]} = "{_post[f[6][0]]}",
    {f[7][2]} = "{_post[f[7][0]]}",
    {f[8][2]} = "{_post[f[8][0]]}",
    {f[9][2]} = ''' + (_post[f[9][0]] if f[9][0] in _post and _post[f[9][0]] else 'NULL') + f''',
    {f[10][2]} = ''' + (_post[f[10][0]] if f[10][0] in _post and _post[f[10][0]] else 'NULL') + f''',
    {f[11][2]} = ''' + (f'"{escape(_post[f[11][0]])}"' if f[11][0] in _post and _post[f[11][0]] else 'NULL') + f'''
WHERE {f[0][2]} = {_id}'''
    with connection.cursor() as cursor:
        cursor.execute(query)


def edit_track(f: list, _post, _id: int):
    track = fields()[23][2]
    query = f'''UPDATE {track} SET
    {f[2][2]} = "{escape(_post[f[2][0]])}",
    {f[3][2]} = ''' + (f'"{escape(_post[f[3][0]])}"' if f[3][0] in _post and _post[f[3][0]] else 'NULL') + f''',
    {f[4][2]} = ''' + (f'"{escape(_post[f[4][0]])}"' if f[4][0] in _post and _post[f[4][0]] else 'NULL') + f''',
    {f[5][2]} = {_post[f[5][0]]},
    {f[6][2]} = {_post[f[6][0]]},
    {f[7][2]} = "{_post[f[7][0]]}",
    {f[12][2]} = ''' + (f'"{escape(_post[f[12][0]])}"' if f[12][0] in _post and _post[f[12][0]] else 'NULL') + f'''
WHERE {f[0][2]} = {_id}'''
    with connection.cursor() as cursor:
        cursor.execute(query)
    for i in (1, 8, 9, 10, 11):
        t = f[i][2] if i < 11 else f'{track}_{f[i][2]}'
        query = f'''DELETE FROM {t}\nWHERE {track}_{f[0][2]} = {_id}'''
        with connection.cursor() as cursor:
            cursor.execute(query)
        if f[i][0] in _post and _post[f[i][0]]:
            for iid in _post.getlist(f[i][0]):
                if iid:
                    with connection.cursor() as cursor:
                        cursor.execute(f'INSERT INTO {t} VALUES ({_id}, {iid})')
