from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .del_ import del_, relationships
from .redirect_ import redirect_
from .Album import Album
from .ISPager.ShowResult import ShowResult
from .show_del_query import get_show_del_query
from .format_td import format_td
from .head_sort_link import django_head_sort_link
from .forms import RppForm


def form_del_album(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefDAl' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 13, 14, 2, 3, 4, 15, 16, 17, 18, 19, 12])
    if request.method == 'POST':
        if 'ok' in request.POST:
            del_(5, _id)
        return redirect_(request, 'MrefDAl', fields()[5][2])
    album = Album(cf, 1, _id)
    cnt = relationships(5, _id)
    rel_data = None
    if len(cnt):
        rel_data = []
        tf = cur_fields(list(range(13)))
        sr = ShowResult(get_show_del_query(5, tf, _id), request)
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
            'caption': f'Найдены связи с {fields()[23][1].lower()}ами, содержащимися в {fields()[5][1].lower()}е',
            'th': [django_head_sort_link(request, sr.getParams(), f) for f in tf if f[0] != tf[cnt[0]][0]],
            'records': records,
            'isp': sr.getISP(),
            'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
            'no_ok': True
        })
    templ_name = f'del.html'
    context = {
        'caption': f'Удаление {fields()[5][1].lower()}а',
        'data': [[cf[i][1], format_td(val)] for i, val in enumerate(album.get_all())],
        'rel_data': rel_data
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefDAl', set_ref, 900)
        return response
    return render(request, templ_name, context)
