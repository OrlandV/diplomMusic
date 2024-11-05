from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .del_ import del_, relationships
from .redirect_ import redirect_
from .OSTFrom import OSTFrom
from .ISPager.ShowResult import ShowResult
from .show_del_query import get_show_del_query
from .format_td import format_td
from .head_sort_link import django_head_sort_link
from .forms import RppForm


def form_del_ost_from(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefDO' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 2, 3, 4, 13])
    if request.method == 'POST':
        if 'ok' in request.POST:
            del_(11, _id)
        return redirect_(request, 'MrefDO', fields()[11][2])
    ost = OSTFrom(cf, _id)
    cnt = relationships(11, _id)
    rel_data = None
    if len(cnt):
        rel_data = []
        tf = cur_fields(list(range(13)))
        sr = ShowResult(get_show_del_query(11, tf, _id), request)
        records = []
        for record in sr.getISP().getItems(request.GET):
            temp = []
            for f in record:
                temp.append(format_td(str(f)) if f is not None else '')
            ed = [
                f'<a href="/music/edit/{fields()[23][2]}/{record[0]}/"><img src="/static/img/pencil.png" /></a>',
                f'<a href="/music/del/{fields()[23][2]}/{record[0]}/" class="adel" style="color: red;">×</a>'
            ]
            temp.append(ed)
            records.append(temp)
        rel_data.append({
            'caption': f'Найдены связи с {fields()[23][1].lower()}ами, входящими в ОСТ',
            'th': [django_head_sort_link(request, sr.getParams(), f) for f in tf if f[0] != tf[cnt[0]][0]],
            'records': records,
            'isp': sr.getISP(),
            'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
            'no_ok': False
        })
    templ_name = f'del.html'
    context = {
        'caption': f'Удаление из «{fields()[11][1]}»',
        'data': [[cf[i][1], format_td(val)] for i, val in enumerate(ost.get_all())],
        'rel_data': rel_data
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefDO', set_ref, 900)
        return response
    return render(request, templ_name, context)
