def show_errors(errors: list, caption: str = 'ОШИБКА!') -> str:
    """
    Конструктор сообщения об ошибке(ах).
    """
    res = f'\n<p class="err">\n\t{caption}<br>\n'
    for err in errors:
        res += f'\t{err}<br>\n'
    return res + '</p>'
