from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .add_album import add_album
from .get_param import get_param
from .sub_sort import sub_sort
from .ISPager.ShowResult import ShowResult
from .show_album_query import get_show_album_query
from .head_sort_link import django_head_sort_link
from .format_td import format_td
from .classes import *
from .forms import RppForm, OMSForm
from .show_errors import show_errors


def form_album(request, cf: list) -> Form:
    def note(text):
        return f' <span class="font80">({text})</span>'

    dp = {}
    for i, f in enumerate(cf):
        if i == 0:
            dp[f[0]] = {
                'label': f[1],
                'type': 'date',
                'required': True
            }
        elif i in (1, 3, 4, 5, 11):
            dp[f[0]] = {
                'label': f[1],
                'type': 'text',
                'required': True if i == 3 else False,
                'size': 200 if f[3] > 200 else f[3],
                'note': note(f'до {f[3]} символов')
            }
        elif i in (6, 7):
            dp[f[0]] = {
                'label': f[1],
                'type': 'number',
                'required': True,
                'min': 1,
                'step': 1,
                'value': 1
            }
        elif i in (8, 9, 10):
            dp[f[0]] = {
                'label': f[1],
                'type': 'selOpt',
                'required': True if i == 8 else False,
                'fields': '*',
                'table': f[2],
                'option': fields()[20][2]
            }
    return Form(request, dp)


def show(request, cf: list, set_ref: str | bool, err: list | None = None) -> HttpResponse:
    af = cur_fields([0])
    af.extend(cf)
    sr = ShowResult(get_show_album_query(af, request.GET), request)
    if items := sr.getISP().getItems(request.GET):
        records = []
        for record in items:
            temp = []
            for f in record:
                temp.append(format_td(f) if f is not None else '')
            ed = [
                f'<a href="/music/edit/{fields()[5][2]}/{record[0]}/"><img src="/static/img/pencil.png" /></a>',
                f'<a href="/music/del/{fields()[5][2]}/{record[0]}/" class="adel" style="color: red;">×</a>'
            ]
            temp.append(ed)
            records.append(temp)
    else:
        records = False
    templ_name = f'add_{fields()[5][2]}.html'
    context = {
        'caption': [fields(True)[5][1], f'Добавление {fields()[5][1].lower()}а'],
        'th': [django_head_sort_link(request, sr.getParams(), f) for f in af],
        'records': records,
        'isp': sr.getISP(),
        'options': [Option(f[0], f[1]) for f in cf],
        'form_oms': OMSForm(),
        'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
        'adds': [{'name': fields()[i][2], 'caption': fields()[i][1]} for i in (17, 18, 19)],
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_add': form_album(request, cf)
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefAddT', set_ref, 3600)
        return response
    return render(request, templ_name, context)


def form_add_album(request):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefAddT' not in request.COOKIES and referrer and 'add/' + fields()[23][2] in referrer:
        set_ref = referrer
    cf = cur_fields([13, 14, 11, 2, 3, 4, 15, 16, 17, 18, 19, 12])
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (2, 3, 4, 12, 14))):
                add_album(request.POST, cf)
                re_params = get_param(request.GET)
                # if 'page' in request.GET:
                #     re_params['page'] = request.GET.get('page')
                return redirect(request.path + ('?' + re_params.urlencode() if len(re_params) else ''))
            return show(request, cf, set_ref, err)
        elif 'rppOK' in request.POST:
            re_params = get_param(request.GET)
            re_params['rpp'] = request.POST.get('rpp')
            return redirect(request.path + ('?' + re_params.urlencode() if len(re_params) else ''))
        elif 'subSort' in request.POST:
            return sub_sort(request)
        elif 'subBack' in request.POST:
            re_params = get_param(request.GET)
            if 'MrefAddT' in request.COOKIES:
                re_params.pop('page', '')
                re_params.pop('sort', '')
                ref = request.COOKIES['MrefAddT']
                if len(re_params):
                    ref += ('&' if '?' in ref else '?') + re_params.urlencode()
                response = redirect(ref)
                response.delete_cookie('MrefAddT')
                return response
            return redirect(f'/music/add/{fields()[23][2]}/' + ('?' + re_params.urlencode() if len(re_params) else ''))
    return show(request, cf, set_ref)
