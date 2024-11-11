from django.http import QueryDict
from urllib.parse import urlencode, parse_qs


def head_sort_link(request, params: str, field: list) -> tuple[str, str]:
    """
    Формирование URI-запроса сортировки для заголовка колонки таблицы + текста заголовка.
    :param request: Объект request.
    :param params: Строка GET-параметров объекта пагинатора (ISPager.Pager.getParams()).
    :param field: Элемент списка fields().
    :return: Кортеж из строки URI-запроса и заголовка колонки.
    """
    def modify_params(params_dict):
        keys_iter = list(params_dict.keys())
        for key in keys_iter:
            if key.startswith('sel'):
                del params_dict[key]
        if 'sub' in params_dict and params_dict['sub'] == 'sort':
            params_dict['sub'] = 'ok'
        return params_dict

    params = modify_params(parse_qs(params))
    sort_param = request.GET.get('sort', '')
    if sort_param:
        params['sort'] = field[0] + ('d' if sort_param == field[0] + 'a' else 'a')
    else:
        params['sort'] = field[0] + 'a'
    return urlencode(params, doseq=True), field[1]


def django_head_sort_link(request, params: str, field: list) -> tuple[str, str]:
    """
    Формирование URI-запроса сортировки для заголовка колонки таблицы + текста заголовка.
    Аналог функции head_sort_link, в котором вместо urllib.parse используется django.http.QueryDict.
    :param request: Объект request.
    :param params: Строка GET-параметров объекта пагинатора (ISPager.Pager.getParams()).
    :param field: Элемент списка fields().
    :return: Кортеж из строки URI-запроса и заголовка колонки.
    """
    def modify_params(params_dict: QueryDict) -> QueryDict:
        keys_iter = list(params_dict.keys())
        for key in keys_iter:
            if key.startswith('sel'):
                params_dict.pop(key)
        if 'sub' in params_dict and params_dict['sub'] == 'sort':
            params_dict['sub'] = 'ok'
        return params_dict

    params = modify_params(QueryDict(params, mutable=True))
    sort_param = request.GET.get('sort', '')
    if sort_param:
        params['sort'] = field[0] + ('d' if sort_param == field[0] + 'a' else 'a')
    else:
        params['sort'] = field[0] + 'a'
    return params.urlencode(), field[1]
