from django.http import QueryDict


def get_param(_get: QueryDict) -> QueryDict:
    res = QueryDict(mutable=True)
    res.update(_get)
    # res.pop('page', '')
    keys = list(res.keys())
    for k in keys:
        if res[k] == '':
            res.pop(k)
    return res


def edit_get(request, *keys: str):
    if request.GET:
        for key in keys:
            if request.GET[key]:
                request.GET.pop(key)
