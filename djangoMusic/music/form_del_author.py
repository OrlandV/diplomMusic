from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .del_ import relationships, del_
from .redirect_ import redirect_
from .Author import Author
from .ISPager.django_pager import get_django_pager
from .show_del_query import get_show_del_query
from .format_td import format_td
from .head_sort_link import django_head_sort_link
from .forms import RppForm


def form_del_author(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefDA' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 21, 22])
    if request.method == 'POST':
        if 'ok' in request.POST:
            del_(24, _id)
        return redirect_(request, 'MrefDA', fields()[24][2])
    author = Author(cf, 1, aid=_id)
    cnt = relationships(24, _id)
    rel_data = None
    if len(cnt):
        rel_data = []
        for c in cnt:
            tf = cur_fields(list(range(13)))
            django_pager = get_django_pager(get_show_del_query(24, tf, _id, c), request)
            records = []
            for record in django_pager.getItems(request.GET):
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
                'caption': f'Найдены связи с {fields()[23][1].lower()}ами, '
                           f'где {fields()[24][1].lower()} является {fields()[c][1][:-3].lower()}ом',
                'th': [django_head_sort_link(request, django_pager.getParameters(), f) for f in tf if f[0] != tf[c][0]],
                'records': records,
                'isp': django_pager,
                'form_rpp': RppForm(request.GET) if 'rpp' in request.GET else RppForm(),
                'no_ok': False
            })
    templ_name = f'del.html'
    context = {
        'caption': f'Удаление {fields()[24][1].lower()}а',
        'data': [[cf[i][1], format_td(val)] for i, val in enumerate(author.get_all())],
        'rel_data': rel_data
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefDA', set_ref, 900)
        return response
    return render(request, templ_name, context)
