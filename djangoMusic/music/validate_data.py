from re import escape
from .fields import fields


def validate_data(_post, ti: tuple) -> bool | list:
    err = []
    for i in ti:
        field = fields()[i][0]
        text = fields()[i][1]
        limit = fields()[i][3]
        if field in _post and len(escape(_post.get(field))) > limit:
            err.append(f'«<tt>{text}</tt>» должно быть не более <tt>{limit}</tt> символов.')
    return False if len(err) == 0 else err
