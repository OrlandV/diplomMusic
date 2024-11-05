from django.db import connection
from re import escape
from .fields import fields


def edit_album(f, _post, _id):
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
