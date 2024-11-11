"""
Представление одной из трёх страниц:
1) «Удаление медиа-формата» по адресу /music/del/media_format/<int:_id>/,
2) «Удаление лейбла» по адресу /music/del/label/<int:_id>/,
3) «Удаление изготовителя» по адресу /music/del/manufacturer/<int:_id>/.
"""
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .del_ import del_, relationships
from .redirect_ import redirect_
from .Name import Name
from .ISPager.django_pager import get_django_pager
from .show_del_query import get_show_del_query
from .format_td import format_td
from .head_sort_link import django_head_sort_link
from .forms import RppForm


def form_del_name(request, index: int, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefDN' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 20])
    if request.method == 'POST':
        if 'ok' in request.POST:
            del_(index, _id)
        return redirect_(request, 'MrefDN', fields()[index][2])
    n = Name(cf, index, _id)
    cnt = relationships(index, _id)
    rel_data = None
    if len(cnt):
        rel_data = []
        af = cur_fields([0, 13, 14, 11, 2, 3, 4, 15, 16, 17, 18, 19, 12])
        django_pager = get_django_pager(get_show_del_query(index, af, _id), request)
        records = []
        for record in django_pager.getItems(request.GET):
            temp = []
            for f in record:
                temp.append(format_td(str(f)) if f is not None else '')
            ed = [
                f'<a href="/music/edit/{fields()[5][2]}/{record[0]}/"><img src="/static/img/pencil.png" /></a>',
                f'<a href="/music/del/{fields()[5][2]}/{record[0]}/" class="adel" style="color: red;">×</a>'
            ]
            temp.append(ed)
            records.append(temp)
        rel_data.append({
            'caption': f'Найдены связи с {fields()[5][1].lower()}ами',
            'th': [django_head_sort_link(request, django_pager.getParameters(), f) for f in af
                   if f[0] != fields()[cnt[0]][0]],
            'records': records,
            'isp': django_pager,
            'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
            'no_ok': True
        })
    templ_name = f'del.html'
    context = {
        'caption': f'Удаление ' + (fields()[index][1][:-1].lower() + 'я' if index == 19 else
                                   fields()[index][1].lower() + 'а'),
        'data': [[cf[i][1], format_td(val)] for i, val in enumerate(n.get_all())],
        'rel_data': rel_data
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefDN', set_ref, 900)
        return response
    return render(request, templ_name, context)
