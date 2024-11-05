from django.db import connection
from re import escape
from .fields import fields


def add_album(_post, f):
    query = f'INSERT INTO {fields()[5][2]} VALUES (DEFAULT, "{escape(_post[f[0][0]])}", ' + (
        f'"{escape(_post[f[1][0]])}"' if f[1][0] in _post and _post[f[1][0]] else 'NULL'
    ) + f', "{escape(_post[f[3][0]])}", ' + (
        f'"{escape(_post[f[4][0]])}"' if f[4][0] in _post and _post[f[4][0]] else 'NULL'
    ) + ', ' + (
        f'"{escape(_post[f[5][0]])}"' if f[5][0] in _post and _post[f[5][0]] else 'NULL'
    ) + f', {_post[f[6][0]]}, {_post[f[7][0]]}, {_post[f[8][0]]}, ' + (
        _post[f[9][0]] if f[9][0] in _post and _post[f[9][0]] else 'NULL'
    ) + ', ' + (_post[f[10][0]] if f[10][0] in _post and _post[f[10][0]] else 'NULL') + ', ' + (
        f'"{escape(_post[f[11][0]])}")' if f[11][0] in _post and _post[f[11][0]] else 'NULL)'
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
