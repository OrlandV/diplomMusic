"""
Представление страницы «Добавление автора» по адресу /music/add/author/.
"""
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .add import add_author
from .get_param import get_param
from .sub_sort import sub_sort
from .ISPager.django_pager import get_django_pager
from .dp_query import get_dp_query
from .head_sort_link import django_head_sort_link
from .format_td import format_td
from .classes import *
from .forms import RppForm, OMSForm
from .show_errors import show_errors


def form_author(request, cf: list) -> Form:
    dp = {}
    for i, f in enumerate(cf):
        dp[f[0]] = {
            'label': f[1],
            'type': 'text',
            'required': False if i else True,
            'size': f[3],
            'note': f' <span class="font80">(до {f[3]} символов)</span>'
        }
    return Form(request, dp)


def show(request, cf: list, set_ref: str | bool, err: list | None = None) -> HttpResponse:
    table = fields()[24][2]
    af = cur_fields([0])
    af.extend(cf)
    django_pager = get_django_pager(get_dp_query(af, request.GET, table), request)
    records = False
    if items := django_pager.getItems(request.GET):
        records = []
        for record in items:
            temp = []
            for f in record:
                temp.append(format_td(str(f)) if f is not None else '')
            ed = [
                f'<a href="/music/edit/{table}/{record[0]}/"><img src="/static/img/pencil.png" /></a>',
                f'<a href="/music/del/{table}/{record[0]}/" class="adel" style="color: red;">×</a>'
            ]
            temp.append(ed)
            records.append(temp)
    templ_name = f'add1.html'
    context = {
        'caption': [fields(True)[24][1], f'Добавление {fields()[24][1].lower()}а'],
        'th': [django_head_sort_link(request, django_pager.getParameters(), f) for f in af],
        'records': records,
        'isp': django_pager,
        'options': [Option(f[0], f[1]) for f in cf],
        'form_oms': OMSForm(),
        'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_add': form_author(request, cf)
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefAddT', set_ref, 900)
        return response
    return render(request, templ_name, context)


def form_add_author(request):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefAddT' not in request.COOKIES and referrer and 'add/' + fields()[23][2] in referrer:
        set_ref = referrer
    cf = cur_fields([21, 22])
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (21, 22))):
                add_author(request.POST, cf)
                re_params = get_param(request.GET)
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
