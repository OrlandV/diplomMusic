from django.db import connection
from re import escape
from .fields import fields


def edit_name(index: int, f, _post, _id: int):
    query = f'''UPDATE {fields()[index][2]} SET
    {f[1][2]} = "{escape(_post[f[1][0]])}"
WHERE {f[0][2]} = {_id}'''
    with connection.cursor() as cursor:
        cursor.execute(query)
