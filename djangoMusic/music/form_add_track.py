from django.shortcuts import redirect, render
from .fields import *
from .validate_data import validate_data
from .add_track import add_track
from .get_param import get_param
from .sub_sort import sub_sort
from .ISPager.ShowResult import ShowResult
from .show_track_query import get_show_track_query
from .head_sort_link import django_head_sort_link
from .format_td import format_td
from .classes import *
from .forms import RppForm, OMSForm
from .show_errors import show_errors
from .album_query import get_album_query
from .author_query import get_author_query


def form_track(request, tcf: list) -> Form:
    def note(text: str) -> str:
        return f' <span class="font80">({text})</span>'

    alf = cur_fields([0, 2, 3, 4, 13, 14, 17, 18])
    auf = cur_fields([0, 21, 22])
    table_author = get_author_query(auf, 1)
    option_author = get_author_query(auf, 4)
    dp = {}
    for i, f in enumerate(tcf):
        if i in (0, 4, 7, 8, 9, 10):
            dp[f[0]] = {
                'label': f[1],
                'type': 'selOpt',
                'multiple': False if i == 4 else True,
                'required': False if i == 4 else True,
                'size': 0 if i == 4 else 6,
                'fields': '*',
                'table': get_album_query(alf, 2) if i == 4 else (f[2] if i == 10 else table_author),
                'option': (get_album_query(alf, 3) if i == 4 else
                           [alf[1][2], alf[2][2], alf[3][2], alf[4][2]]) if i in (4, 10) else option_author,
                'sort': fields()[3][2] if i == 10 else fields()[22][2],
                'optionWidth': 198,
                'note': note('множественный выбор с помощью CTRL и SHIFT') if i not in (4, 10) else ""
            }
            if i not in (4, 10):
                dp[f[0]]['separator'] = ' / '
        elif i in (1, 2, 3, 11):
            dp[f[0]] = {
                'label': f[1],
                'type': 'text',
                'required': True if i == 1 else False,
                'size': 200 if f[3] > 200 else f[3],
                'note': note(f'до {f[3]} символов')
            }
        elif i == 5:
            dp[f[0]] = {
                'label': f[1],
                'type': 'number',
                'required': True,
                'min': 1,
                'step': 1,
                'value': 1
            }
        elif i == 6:
            dp[f[0]] = {
                'label': f[1],
                'type': 'time',
                'required': True,
                'step': 1
            }
    return Form(request, dp)


def show(request, cf: list, err: list | None = None):
    sr = ShowResult(get_show_track_query(cf, request.GET), request)
    if items := sr.getISP().getItems(request.GET):
        records = []
        for record in items:
            temp = []
            for f in record:
                temp.append(format_td(str(f)) if f is not None else '')
            ed = [
                f'<a href="/music/edit/{fields()[23][2]}/{record[0]}/"><img src="/static/img/pencil.png" /></a>',
                f'<a href="/music/del/{fields()[23][2]}/{record[0]}/" class="adel" style="color: red;">×</a>'
            ]
            temp.append(ed)
            records.append(temp)
    else:
        records = False
    return render(request, f'add_{fields()[23][2]}.html', {
        'caption': [fields(True)[23][1], f'Добавление {fields()[23][1].lower()}а'],
        'th': [django_head_sort_link(request, sr.getParams(), f) for f in cf],
        'records': records,
        'isp': sr.getISP(),
        'options': [Option(f[0], f[1]) for f in cf],
        'form_oms': OMSForm(),
        'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
        'adds': [{'name': fields()[i][2], 'caption': fields()[i][1]} for i in (24, 5, 11)],
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_add': form_track(request, cf[1:])
    })


def form_add_track(request):
    cf = cur_fields(list(range(13)))
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (2, 3, 4, 12))):
                add_track(request.POST, cf[1:])
                re_params = get_param(request.GET)
                # if 'page' in request.GET:
                #     re_params['page'] = request.GET.get('page')
                return redirect(request.path + ('?' + re_params.urlencode() if len(re_params) else ''))
            return show(request, cf, err)
        elif 'rppOK' in request.POST:
            re_params = get_param(request.GET)
            re_params['rpp'] = request.POST.get('rpp')
            return redirect(request.path + ('?' + re_params.urlencode() if len(re_params) else ''))
        elif 'subSort' in request.POST:
            return sub_sort(request)
    return show(request, cf)
