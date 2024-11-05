from django.db import connection
from re import escape
from .fields import fields


def add_track(_post, f):
    track = fields()[23][2]
    query = f'INSERT INTO {track} VALUES (DEFAULT, "'
    query += escape(_post.get(f[1][0])) + '", '
    query += (f'"{escape(_post.get(f[2][0]))}"' if f[2][0] in _post and _post[f[2][0]] else 'NULL') + ', '
    query += (f'"{escape(_post.get(f[3][0]))}"' if f[3][0] in _post and _post[f[3][0]] else 'NULL') + ', '
    query += _post.get(f[4][0]) + ', '
    query += _post.get(f[5][0]) + ', "'
    query += _post.get(f[6][0]) + '", '
    query += (f'"{escape(_post.get(f[11][0]))}")' if f[11][0] in _post and _post[f[11][0]] else 'NULL)')
    with connection.cursor() as cursor:
        cursor.execute(query)
        tid = cursor.lastrowid
    for i in (0, 7, 8, 9, 10):
        if f[i][0] in _post and _post[f[i][0]]:
            for _id in _post.getlist(f[i][0]):
                if _id:
                    t = f[i][2] if i < 10 else f'{track}_{f[i][2]}'
                    with connection.cursor() as cursor:
                        cursor.execute(f'INSERT INTO {t} VALUES ({tid}, {_id})')
