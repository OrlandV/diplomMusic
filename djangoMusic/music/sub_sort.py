from django.http import QueryDict
from django.shortcuts import redirect


def sub_sort(request):
    """
    Построение URI-строки (GET-параметров) из POST-параметров формы множественной сортировки
    и переадресация уже с новой URI-строкой.
    :param request: Объект django.http.request.
    """
    params = QueryDict(request.META['QUERY_STRING'], mutable=True)
    if 'page' in params:
        params.pop('page')
    if 'sort' in params:
        params.pop('sort')
    params['sub'] = 'sort'
    params['sel'] = request.POST.get('selSort', '')
    if 'chbSort' in request.POST:
        params['chb'] = request.POST.get('chbSort')
    i = 1
    while True:
        sel_sort_value = request.POST.get(f'selSort{i}', '')
        if sel_sort_value == '':
            break
        params[f'sel{i}'] = sel_sort_value
        chb_sort_key = f'chbSort{i}'
        if chb_sort_key in request.POST:
            params[f'chb{i}'] = request.POST.get(chb_sort_key)
        i += 1
    return redirect(f'{request.path}?{params.urlencode()}')
