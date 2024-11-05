from .fields import *
from .author_query import get_author_query


def track_query(cf: list, rel: int = 0, where: str = '') -> str:
    """
    Формирование tables-фрагмента SQL-запроса для объекта ShowResult.
    :param cf: Список элементов HTML-формы, содержащих соответствующие имена полей в БД.
        Является результатом функции cur_fields.
    :param rel: Индекс связи (1, 5, 8, 9, 10, 11). Используется для выключения удаляемой сущности при отображении связи.
    :param where: WHERE-параметр фильтра при удалении.
    :return: Строка фрагмента SQL-запроса.
    """
    f0 = cf[0][2]  # id
    f1 = cf[1][2]  # performer
    f2 = cf[2][2]  # name_original
    f3 = cf[3][2]  # name_romaji
    f4 = cf[4][2]  # name_english
    f5 = cf[5][2]  # album
    f6 = cf[6][2]  # number_in_album
    f7 = cf[7][2]  # duration
    f8 = cf[8][2]  # lyricist
    f9 = cf[9][2]  # composer
    f10 = cf[10][2]  # arranger
    f11 = cf[11][2]  # ost_from
    f12 = cf[12][2]  # notes
    f23 = fields()[23][2]  # track
    af = cur_fields([0, 21, 22])
    gcd = 'GROUP_CONCAT(DISTINCT '
    lj = 'LEFT JOIN '
    s = '(\n\t\tSELECT '
    sa = " SEPARATOR ', ') AS "
    return f'''{s}{f23}.{f0} AS {f0},
        ''' + ('' if rel == 1 else f'''{gcd}{f23}_{f1}.{f1}{sa}{f1},
        ''') + f'''{f23}.{f2} AS {f2},
        {f23}.{f3} AS {f3},
        {f23}.{f4} AS {f4},
        ''' + ('' if rel == 5 else f'''IF(
            {f5}.{f3} IS NULL,
            {f5}.{f2},
            {f5}.{f3}
        ) AS {f5},
        ''') + f'''{f23}.{f6} AS {f6},
        {f23}.{f7} AS {f7},
        ''' + ('' if rel == 8 else f'''{gcd}{f23}_{f8}.{f8}{sa}{f8},
        ''') + ('' if rel == 9 else f'''{gcd}{f23}_{f9}.{f9}{sa}{f9},
        ''') + ('' if rel == 10 else f'''{gcd}{f23}_{f10}.{f10}{sa}{f10},
        ''') + ('' if rel == 11 else f'''{gcd}{f11}.{f3}{sa}{f11},
        ''') + f'''{f23}.{f12} AS {f12}
    FROM {f23}
    ''' + ('' if rel == 1 else f'''{lj}{get_author_query(af, 3, index=1)}
    ON {f23}.{f0} = {f23}_{f1}.{f0}
    ''') + ('' if rel == 5 else f'''INNER JOIN {f5}
    ON {f23}.{f5} = {f5}.{f0}
    ''') + ('' if rel == 8 else f'''{lj}{get_author_query(af, 3, index=8)}
    ON {f23}.{f0} = {f23}_{f8}.{f0}
    ''') + ('' if rel == 9 else f'''{lj}{get_author_query(af, 3, index=9)}
    ON {f23}.{f0} = {f23}_{f9}.{f0}
    ''') + ('' if rel == 10 else f'''{lj}{get_author_query(af, 3, index=10)}
    ON {f23}.{f0} = {f23}_{f10}.{f0}
    ''') + ('' if rel == 11 else f'''{lj}{f23}_{f11}
    ON {f23}.{f0} = {f23}_{f11}.{f23}_{f0}
    {lj}{f11}
    ON {f23}_{f11}.{f11}_{f0} = {f11}.{f0}
    ''') + (f'''INNER JOIN {f23 + '_' if rel == 11 else ''}{cf[rel][2]}
    ON {f23 + '_' + f11 if rel == 11 else ''}.{cf[rel][2] if rel == 5 else
        (f23 + '_' + f0 if rel == 11 else f0)} = {f23 if rel == 11 else
        cf[rel][2]}.{'' if rel in (5, 11) else f23 + '_'}{f0}
    {where}''' if where else '') + f'''
    GROUP BY {f0}
) AS {f23}s'''
