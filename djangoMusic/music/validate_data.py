from re import escape
from .fields import fields


def validate_data(_post, ti: tuple, f: bool = False) -> bool | list:
    err = []
    for i in ti:
        field = fields(f=f)[i]
        if field[0] in _post and len(escape(_post.get(field[0]))) > field[3]:
            err.append(f'«<tt>{field[1]}</tt>» должно быть не более <tt>{field[3]}</tt> символов.')
    return False if len(err) == 0 else err
