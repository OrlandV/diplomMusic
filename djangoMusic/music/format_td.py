from django.utils.html import escape
from django.utils.safestring import mark_safe


def format_td(td: str | int | None, cut: bool = True) -> str:
    """
    Форматирование строки. Содержимое ячейки (td) преобразуется в HTML-безопасную строку.
    Дополнительно проставляются неразрывные пробелы перед символами «—» и «|» и заменяется «\\\\n» на «<br>».
    Если строка длиннее 1022 символов и cut == True, то она обрежется,
    а в конце добавится «<span class="font80">…</span>».
    :param td: Строка, содержащаяся в ячейке таблицы.
    :param cut: Обрезать (True) или нет (False) строку.
    :return: HTML-безопасная строка.
    """
    if not td:
        return ''
    td = str(td)
    string = escape(td)
    string = string.replace(" — ", "&nbsp;— ").replace(" | ", "&nbsp;| ").replace("\n", "<br>")
    if len(td) > 1022 and cut:
        string += '<span class="font80">…</span>'
    return mark_safe(string)
