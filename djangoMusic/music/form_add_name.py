from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .add import add_name
from .get_param import get_param
from .sub_sort import sub_sort
from .ISPager.ShowResult import ShowResult
from .show_name_query import get_show_name_query
from .format_td import format_td
from .head_sort_link import django_head_sort_link
from .classes import *
from .forms import RppForm
from .show_errors import show_errors


def show(request, cf: list, index: int, set_ref: str | bool, err: list | None = None) -> HttpResponse:
    nf = cur_fields([0])
    nf.extend(cf)
    sr = ShowResult(get_show_name_query(index, nf, request.GET), request)
    if items := sr.getISP().getItems(request.GET):
        records = []
        for record in items:
            temp = []
            for f in record:
                temp.append(format_td(str(f)) if f is not None else '')
            ed = [
                f'<a href="/music/edit/{fields()[index][2]}/{record[0]}/"><img src="/static/img/pencil.png" /></a>',
                f'<a href="/music/del/{fields()[index][2]}/{record[0]}/" class="adel" style="color: red;">×</a>'
            ]
            temp.append(ed)
            records.append(temp)
    else:
        records = False
    templ_name = f'add.html'
    context = {
        'caption': [fields(True)[index][1],
                    'Добавление ' + (fields()[index][1][:-1].lower() + 'я' if index == 19 else
                                     fields()[index][1].lower() + 'а')],
        'th': [django_head_sort_link(request, sr.getParams(), f) for f in nf],
        'records': records,
        'isp': sr.getISP(),
        'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_add': Form(request, {cf[0][0]: {
            'label': cf[0][1],
            'type': 'text',
            'required': True,
            'size': cf[0][3],
            'note': f' <span class="font80">(до {cf[0][3]} символов)</span>'
        }})
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefAddAl', set_ref, 900)
        return response
    return render(request, templ_name, context)


def form_add_name(request, index: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefAddAl' not in request.COOKIES and referrer and f'add/{fields()[5][2]}' in referrer:
        set_ref = referrer
    cf = cur_fields([20], True if index == 17 else False)
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (20,))):
                add_name(request.POST, cf, index)
                re_params = get_param(request.GET)
                # if 'page' in request.GET:
                #     re_params['page'] = request.GET.get('page')
                return redirect(request.path + ('?' + re_params.urlencode() if len(re_params) else ''))
            return show(request, cf, index, set_ref, err)
        elif 'rppOK' in request.POST:
            re_params = get_param(request.GET)
            re_params['rpp'] = request.POST.get('rpp')
            return redirect(request.path + ('?' + re_params.urlencode() if len(re_params) else ''))
        elif 'subSort' in request.POST:
            return sub_sort(request)
        elif 'subBack' in request.POST:
            re_params = get_param(request.GET)
            if 'MrefAddAl' in request.COOKIES:
                re_params.pop('page', '')
                re_params.pop('sort', '')
                ref = request.COOKIES['MrefAddAl']
                if len(re_params):
                    ref += ('&' if '?' in ref else '?') + re_params.urlencode()
                response = redirect(ref)
                response.delete_cookie('MrefAddAl')
                return response
            return redirect(f'/music/add/{fields()[5][2]}/' + ('?' + re_params.urlencode() if len(re_params) else ''))
    return show(request, cf, index, set_ref)