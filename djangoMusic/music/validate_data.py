from re import escape
from .fields import fields


def validate_data(_post, ti: tuple, f: bool = False) -> bool | list:
    """
    Проверка введённых данных на соответствие требованиям.
    Если ошибок ввода нет, возвращается False.
    Иначе — список описаний ошибок.
    :param _post: Словарь POST-параметров.
    :param ti: Кортеж индексов проверяемых полей в списке fields.
    :param f: Флаг f в функции fields.
    """
    err = []
    for i in ti:
        field = fields(f=f)[i]
        if field[0] in _post and len(escape(_post.get(field[0]))) > field[3]:
            err.append(f'«<tt>{field[1]}</tt>» должно быть не более <tt>{field[3]}</tt> символов.')
    return False if not len(err) else err
