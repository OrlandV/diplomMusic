from .fields import fields


def get_author_query(af: list, mode: int | str, _get: dict | None = None, select: bool = True,
                     index: int = 1) -> str | list:
    """
    Формирование tables-фрагмента SQL-запроса для функции get_django_pager.
    :param af: Список элементов HTML-формы, содержащих соответствующие имена полей в БД.
        Является результатом функции cur_fields.
    :param mode: Номер или имя режима запроса.
    :param _get: Словарь GET-параметров.
    :param select: Флаг обёртки "(SELECT …) AS sel_". Выключается в инициализации объекта Author.
    :param index: Индекс роли (1 — вокалист, 8 — поэт, 9 — композитор, 10 — аранжировщик).
    :return: Строка фрагмента SQL-запроса.
    """
    f0 = af[0][2]  # id
    f1 = af[1][2]  # name_original
    f2 = af[2][2]  # name_romaji
    f23 = fields()[23][2]  # track
    f24 = fields()[24][2]  # author
    ta = fields()[index][2]  # performer / lyricist / composer / arranger  (1 / 8 / 9 / 10)
    gb = 'GROUP BY '
    ij = 'INNER JOIN '
    s = '(\n\t\tSELECT '

    if mode in (1, 'table'):
        return (s if select else '') + f'''{f0} AS {f0},
        {f1} AS {f1},
        {f2} AS {f2}
    FROM {f24}''' + (f'''
    {gb}{f0}
) AS sel_{f24}''' if select else '')

    elif mode in (2, 'table_filter'):
        return (s if select else '') + f'''{f24}.{f0} AS {f0},
        {f24}.{f1} AS {f1},
        {f24}.{f2} AS {f2}
    FROM {f24}
    {ij}{ta}
    ON {f24}.{f0} = {ta}.{f24}_{f0}''' + (f'''
    WHERE {ta}.{f23}_{f0} = {_get.get(af[0][0])}
    {gb}{f0}
) AS sel_{f24}''' if select else '')

    elif mode in (3, 'subtable'):
        return f'''{s}{f23}.{f0} AS {f0},
            GROUP_CONCAT(DISTINCT IF(
                {f24}.{f2} IS NULL,
                {f24}.{fields()[21][2]},
                {f24}.{f2}
            ) SEPARATOR ', ') AS {ta}
        FROM {f23}
        {ij}{ta}
        ON {f23}.{f0} = {ta}.{f23}_{f0}
        {ij}{f24}
        ON {ta}.{f24}_{f0} = {f24}.{f0}
        {gb}{f0}
    ) AS {f23}_{ta}'''

    elif mode in (4, 'option'):
        return [f1, f2]
