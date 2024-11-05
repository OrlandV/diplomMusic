from django.db import connection
from re import escape
from .fields import fields


def edit_ost_from(f, _post, _id):
    query = f'''UPDATE {fields()[11][2]} SET
    {f[1][2]} = "{escape(_post[f[1][0]])}",
    {f[2][2]} = ''' + (f'"{escape(_post[f[2][0]])}"' if f[2][0] in _post and _post[f[2][0]] else 'NULL') + f''',
    {f[3][2]} = ''' + (f'"{escape(_post[f[3][0]])}"' if f[3][0] in _post and _post[f[3][0]] else 'NULL') + f''',
    {f[4][2]} = "{_post[f[4][0]]}"
WHERE {f[0][2]} = {_id}'''
    with connection.cursor() as cursor:
        cursor.execute(query)
