from django.db import connection


def dict_fetch_all(query: str, all_one: bool = False) -> list[dict] | dict:
    """
    Преобразование строк курсора (кортежей) в словари.
    (Идея функции взята из документации Django.)
    :param query: Строка SQL-запроса.
    :param all_one: Переключатель между fetchall (False) и fetchone (True).
    :return: Если all_one == True, то возвращает словарь с результатом запроса (dict).
        Если all_one == False, то возвращает список словарей с результатами запроса (list[dict]).
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        if all_one:
            return dict(zip(columns, cursor.fetchone()))
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
