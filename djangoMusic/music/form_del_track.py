"""
Представление страницы «Удаление трека» по адресу /music/del/track/<int:_id>/.
"""
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .del_ import del_
from .redirect_ import redirect_
from .Track import Track
from .format_td import format_td


def form_del_track(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefDT' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields(list(range(13)))
    if request.method == 'POST':
        if 'ok' in request.POST:
            del_(23, _id)
        return redirect_(request, 'MrefDT', fields()[23][2])
    track = Track(cf, _id)
    templ_name = f'del.html'
    context = {
        'caption': f'Удаление {fields()[23][1].lower()}а',
        'data': [[cf[i][1], format_td(val)] for i, val in enumerate(track.get_all())]
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefDT', set_ref, 900)
        return response
    return render(request, templ_name, context)
