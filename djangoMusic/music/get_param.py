from django.http import QueryDict


def get_param(_get: QueryDict) -> QueryDict:
    """
    Очистка словаря GET-параметров от пустых элементов.
    """
    res = QueryDict(mutable=True)
    res.update(_get)
    keys = list(res.keys())
    for k in keys:
        if res[k] == '':
            res.pop(k)
    return res
