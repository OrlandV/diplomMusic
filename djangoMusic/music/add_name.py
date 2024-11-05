from django.db import connection
from re import escape
from .fields import fields


def add_name(_post, f: list, index: int):
    query = f'INSERT INTO {fields()[index][2]} VALUES (DEFAULT, "{escape(_post[f[0][0]])}")'
    with connection.cursor() as cursor:
        cursor.execute(query)
