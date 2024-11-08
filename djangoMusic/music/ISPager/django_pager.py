from django.http import QueryDict
from .DjangoPager import DjangoPager
from .ItemsRange import ItemsRange


def verification(query):
    err = []
    if not isinstance(query, dict):
        err.append('Вторым аргументом должен быть словарь параметров SQL-запроса.')
    else:
        for k, v in query.items():
            if k not in ('tables', 'fields', 'where', 'group', 'order'):
                err.append("В качестве ключей словаря параметров SQL-запроса ожидаются только 'tables', 'fields', "
                           "'where', 'group', 'order'.")
        if len(query) != 5:
            err.append("Необходимо указать все 5 параметров ('tables', 'fields', 'where', 'group', 'order'). "
                       "Если нужно пропустить параметр, тогда укажите пустое значение '' (например 'order': '').")
    if len(err):
        print('Ошибка инициализации ShowResult')
        for e in err:
            print(e)
        return False
    return True


def get_django_pager(query: dict, request) -> DjangoPager:
    if verification(query):
        params = QueryDict(mutable=True)
        params.update(request.GET)
        params.pop('page', '')
        return DjangoPager(
            view=ItemsRange(request),
            table_name=query['tables'],
            fields=query['fields'],
            where=query['where'],
            group=query['group'],
            order=query['order'],
            items_per_page=int(request.GET.get('rpp')) if request.GET.get('rpp', '') != '' else 10,
            links_count=3,
            get_params=params.urlencode(),
            counter_param='page'
        )
