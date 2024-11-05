from django.db import connection
from re import escape
from .fields import fields


def edit_track(f: list, _post, _id):
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
