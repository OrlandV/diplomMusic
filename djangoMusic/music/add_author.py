from django.db import connection
from re import escape
from .fields import fields


def add_author(_post, f):
    query = f'INSERT INTO {fields()[24][2]} VALUES (DEFAULT, "{escape(_post[f[0][0]])}", ' + (
        f'"{escape(_post[f[1][0]])}")' if f[1][0] in _post and _post[f[1][0]] else 'NULL)'
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
