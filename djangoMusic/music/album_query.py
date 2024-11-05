from .fields import fields


def get_album_query(af: list, mode: int | str, aid: int = 0, rel: int = 0, where: str = '') -> str:
    ff5 = fields()[5][2]  # album
    ff20 = fields()[20][2]  # name
    f0 = fields()[0][2]  # id
    f1 = fields()[13][2]  # date
    f2 = fields()[14][2]  # catalog_number
    f4 = fields()[2][2]  # name_original
    f5 = fields()[3][2]  # name_romaji
    f6 = fields()[4][2]  # name_english
    f9 = fields()[17][2]  # media_format
    f10 = fields()[18][2]  # label
    s = "SELECT "
    lj = "LEFT JOIN "

    if mode in (1, 'table'):
        ff23 = fields()[23][2]  # track
        f3 = fields()[11][2]  # ost_from
        f7 = fields()[15][2]  # count_of_discs
        f8 = fields()[16][2]  # count_of_tracks
        f11 = fields()[19][2]  # manufacturer
        f12 = fields()[12][2]  # notes
        return (s if aid else f'''(
    {s}{ff5}.{f0} AS {f0},
        ''') + f'''{ff5}.{f1} AS {f1},
        {ff5}.{f2} AS {f2},
        ''' + (f'''GROUP_CONCAT(DISTINCT IF(
            {f3}.{f5} IS NULL,
            {f3}.{f4},
            {f3}.{f5}
        ) SEPARATOR ', ') AS {f3},
        ''' if fields()[11] in af else '') + f'''{ff5}.{f4} AS {f4},
        {ff5}.{f5} AS {f5},
        {ff5}.{f6} AS {f6},
        {ff5}.{f7} AS {f7},
        {ff5}.{f8} AS {f8},''' + ('' if rel == 17 else f'''
        {f9}.{ff20} AS {f9},''') + ('' if rel == 18 else f'''
        {f10}.{ff20} AS {f10},''') + ('' if rel == 19 else f'''
        {f11}.{ff20} AS {f11},''') + f'''
        {ff5}.{f12} AS {f12}
    FROM {ff5}
    {lj}{ff23}
    ON {ff5}.{f0} = {ff23}.{ff5}''' + (f'''
    {lj}{ff23}_{f3}
    ON {ff23}.{f0} = {ff23}_{f3}.{ff23}_{f0}
    {lj}{f3}
    ON {ff23}_{f3}.{f3}_{f0} = {f3}.{f0}''' if fields()[11] in af else '') + ('' if rel == 17 else f'''
    {lj}{f9}
    ON {ff5}.{f9} = {f9}.{f0}''') + ('' if rel == 18 else f'''
    {lj}{f10}
    ON {ff5}.{f10} = {f10}.{f0}''') + ('' if rel == 19 else f'''
    {lj}{f11}
    ON {ff5}.{f11} = {f11}.{f0}
    ''') + (f'''WHERE {ff5}.{f0} = {aid}''' if aid else (where if where else '') + f'''
    GROUP BY {f0}
    ORDER BY {f1}, {f2}
) AS {ff5}s''')

    elif mode in (2, 'table_lite'):
        return (s if aid else f'''(
    {s}{ff5}.{f0} AS {f0},
        ''') + f'''{ff5}.{f4} AS {f4},
        {ff5}.{f5} AS {f5},
        {ff5}.{f6} AS {f6},
        {ff5}.{f1} AS {f1},
        {ff5}.{f2} AS {f2},
        {f9}.{ff20} AS {f9},
        {f10}.{ff20} AS {f10}
    FROM {ff5}
    {lj}{f9}
    ON {ff5}.{f9} = {f9}.{f0}
    {lj}{f10}
    ON {ff5}.{f10} = {f10}.{f0}
    ''' + (f'WHERE {ff5}.{f0} = {aid}' if aid else f'''GROUP BY {f0}
    ORDER BY {f5}, {f6}, {f1}, {f2}, {f9}
) AS {ff5}s_lite''')

    elif mode in (3, 'option'):
        return [f4, f5, f6, f1, f2, f9, f10]
