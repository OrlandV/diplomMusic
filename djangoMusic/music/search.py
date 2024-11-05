from django.shortcuts import render, redirect
from django.http import QueryDict
from .fields import *
from .sub_sort import sub_sort
from .search_query import get_search_query
from .ISPager.ShowResult import ShowResult
from .head_sort_link import django_head_sort_link
from .format_td import format_td
from .classes import *
from .forms import RppForm, OMSForm
from .album_query import get_album_query
from .author_query import get_author_query


def sub_ok(request, cf):
    params = QueryDict(mutable=True)
    if 'rppOK' in request.POST:
        params.update(request.GET)
        params['rpp'] = request.POST.get('rpp')
    elif 'ok' in request.POST:
        params['sub'] = 'ok'
        params.update(request.POST)
        params.pop('ok')
        params.pop('csrfmiddlewaretoken')
        for f in cf:
            if f[0] in params and params[f[0]] == '':
                params.pop(f[0])
    return redirect(request.path + ('?' + params.urlencode() if len(params) else ''))


def form_search(request, scf):
    def note(text):
        return f' <span class="font80">({text})</span>'

    alf = cur_fields([0, 2, 3, 4, 13, 14, 17, 18])
    auf = cur_fields([0, 21, 22])
    scf.append(['chbStr', 'Строгий режим&nbsp;&nbsp;<img src="/static/img/quest.png" width="18" height="18" '
                          'class="help-head" onclick="helpClick(\'help-body\');">', '', None])
    table_author = get_author_query(auf, 1)
    option_author = get_author_query(auf, 4)
    dp = {}
    for i, f in enumerate(scf):
        if i in (0, 4, 7, 8, 9, 10):
            dp[f[0]] = {
                'label': f[1],
                'type': 'selOpt',
                'multiple': False if i == 4 else True,
                'size': 0 if i == 4 else 6,
                'fields': '*',
                'table': get_album_query(alf, 2) if i == 4 else (f[2] if i == 10 else table_author),
                'option': (
                    get_album_query(alf, 3) if i == 4 else
                    [alf[1][2], alf[2][2], alf[3][2], alf[4][2]]
                ) if i in (4, 10) else option_author,
                'optionWidth': 198,
                'note': note('множественный выбор с помощью CTRL и SHIFT') if i != 4 else ""
            }
            if i not in (4, 10):
                dp[f[0]].update({'separator': ' / ', 'sort': auf[2][2]})
        elif i in (1, 2, 3, 11):
            dp[f[0]] = {
                'label': f'{f[1]} содержит',
                'type': 'text',
                'size': 200 if f[3] > 200 else f[3],
                'note': note(f'до {f[3]} символов')
            }
        elif i == 6:
            dp[f[0]] = {
                'label': f[1],
                'type': 'time',
                'step': 1
            }
        elif i == 12:
            dp[f[0]] = {
                'type': 'checkbox',
                'chbPar': {
                    'tr_td': True,
                    'label': f[1],
                    'id': 'Str',
                    'on': 'Да',
                    'off': 'Нет'
                }
            }
    return Form(request, dp)


def search(request):
    cf = cur_fields(list(range(13)))
    message = ''
    if request.method == 'POST':
        if 'ok' in request.POST or 'rppOK' in request.POST:
            return sub_ok(request, cf)
        elif 'subSort' in request.POST:
            return sub_sort(request)
    else:
        query = None
        if 'sub' in request.GET and request.GET['sub'] in ('ok', 'sort'):
            if request.GET['sub'] == 'sort' and 'sel' in request.GET and request.GET['sel'] == '':
                message += '<p class="cnt" style="color: yellow;">Укажите хотя бы один параметр для сортировки.</p>\n'
            query = get_search_query(request.GET, cf)
            if not query:
                message += '<p class="cnt" style="color: yellow;">Укажите хотя бы один параметр для поиска.</p>\n'
        if query is None or not query:
            query = get_search_query(request.GET, cf, True)
        sr = ShowResult(query, request)
        if items := sr.getISP().getItems(request.GET):
            records = []
            for record in items:
                temp = []
                for f in record:
                    temp.append(format_td(str(f)) if f is not None else '')
                ed = [
                    f'<a href="edit/{fields()[23][2]}/{record[0]}/"><img src="/static/img/pencil.png" /></a>',
                    f'<a href="del/{fields()[23][2]}/{record[0]}/" class="adel" style="color: red;">×</a>'
                ]
                temp.append(ed)
                records.append(temp)
        else:
            records = False
    return render(request, 'search.html', {
        'caption': 'Поиск',
        'th': [django_head_sort_link(request, sr.getParams(), f) for f in cf],
        'records': records,
        'isp': sr.getISP(),
        'options': [Option(f[0], f[1]) for f in cf],
        'form_oms': OMSForm(),
        'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
        'track_table': {'name': fields()[23][2], 'caption': fields()[23][1].lower()},
        'form_search': form_search(request, cf[1:]),
        'message': message
    })
