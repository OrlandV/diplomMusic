from django.http import QueryDict
from .DjangoPager import DjangoPager
from .ItemsRange import ItemsRange


class ShowResult:
    def __init__(self, query: dict, request):
        if self.verification(query):
            params = QueryDict(mutable=True)
            params.update(request.GET)
            params.pop('page', '')
            self.get_params = params.urlencode()
            self.isp = DjangoPager(
                view=ItemsRange(request),
                table_name=query['tables'],
                fields=query['fields'],
                where=query['where'],
                group=query['group'],
                order=query['order'],
                items_per_page=int(request.GET.get('rpp')) if request.GET.get('rpp', '') != '' else 10,
                links_count=3,
                get_params=self.get_params,
                counter_param='page'
            )

    @staticmethod
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

    def getISP(self):
        return self.isp

    def getParams(self):
        return self.get_params
