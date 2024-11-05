def fields(s: bool = False, f: bool = False) -> list[list[str, str, str, int | None]]:
    """
    Список списков строк (имя (краткое) элемента HTML-формы, текст метки и имя поля в БД)
    и целого числа (размера текстового поля (не будет, если элемент не является текстовым полем)).
    :param s: Флаг окончания множественного числа существительного.
    :param f: Флаг длины строки наименования медиа-формата, лейбла или изготовителя альбома. True — 15, False — 45.
    :return: Пример: [['ident', 'ID', 'id'], …, ['namor', 'Наименование (оригинальное)', 'name_original', 100], …]
    """
    return [
        ['ident', 'ID', 'id'],  # 0
        # track
        ['perfo', 'Вокалист' + ('ы' if s else '(ы)'), 'performer'],  # 1
        # track, album, ost_from
        ['namor', 'Наименование (оригинальное)', 'name_original', 100],  # 2
        ['namro', 'Наименование (ромадзи)', 'name_romaji', 100],  # 3
        ['namen', 'Наименование (английское)', 'name_english', 160],  # 4
        # track
        ['album', 'Альбом' + ('ы' if s else ''), 'album'],  # 5
        ['trnal', 'Номер в альбоме', 'number_in_album'],  # 6
        ['trdur', 'Продолжительность', 'duration'],  # 7
        ['lyric', 'Поэт' + ('ы' if s else '(ы)'), 'lyricist'],  # 8
        ['compo', 'Композитор' + ('ы' if s else '(ы)'), 'composer'],  # 9
        ['arran', 'Аранжировщик' + ('и' if s else '(и)'), 'arranger'],  # 10
        ['ostfr', 'Музыка из', 'ost_from'],  # 11
        # track, album
        ['notes', 'Примечания', 'notes', 380],  # 12
        # album, ost_from
        ['date_', 'Дата релиза или премьеры', 'date'],  # 13
        # album
        ['catnu', 'Каталожный номер', 'catalog_number', 15],  # 14
        ['coudi', 'Количество дисков', 'count_of_discs'],  # 15
        ['coutr', 'Количество трэков', 'count_of_tracks'],  # 16
        ['mefor', 'Медиа-формат' + ('ы' if s else ''), 'media_format'],  # 17
        ['label', 'Лейбл' + ('ы' if s else ''), 'label'],  # 18
        ['manuf', 'Изготовител' + ('и' if s else 'ь'), 'manufacturer'],  # 19
        # media_format, label, manufacturer
        ['name_', 'Наименование', 'name', (15 if f else 45)],  # 20
        # author (performer, lyricist, composer, arranger)
        ['finor', 'ФИО или наименование (оригинальное)', 'name_original', 60],  # 21
        ['finre', 'ФИО или наименование (ромадзи или английское)', 'name_romaji', 65],  # 22

        ['track', 'Трек' + ('и' if s else ''), 'track'],  # 23
        ['autho', 'Автор' + ('ы' if s else ''), 'author']  # 24
    ]


def cur_fields(ai: list, f: bool = False) -> list[list[str, str, str, int | None]]:
    """
    Выборка из fields элементов, индексы которых перечислены в списке ai.
    :param ai: Список индексов элементов из fields, которые требуются в итоговом списке.
    :param f: Флаг f в параметрах fields.
    :return:
    """
    r = []
    for i in ai:
        r.append(fields(False, f)[i])
    return r


def find_field(fn: str) -> str | bool:
    """
    Поиск имени поля в БД по имени элемента HTML-формы.
    :param fn: Имя элемента HTML-формы.
    :return: Имя поля в БД, если оно найдено. Иначе — False.
    """
    for f in fields():
        if f[0] == fn:
            return f[2]
    return False
