from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .edit_album import edit_album
from .redirect_ import redirect_
from .Album import Album
from .format_td import format_td
from .show_errors import show_errors
from .classes import Form


def show(request, cf: list, set_ref: str | bool, _id: int | None = None, err: list | None = None) -> HttpResponse:
    album = Album(cf, 1, _id)
    dp = {}
    for i, f in enumerate(cf):
        if i in (0, 6, 7):
            dp[f[0]] = {
                'label': f[1],
                'type': 'number',
                'disabled': False if i else True,
                'required': True,
                'min': 1,
                'step': 1,
                'value': str(_id) if i == 0 else (album.count_of_discs if i == 6 else album.count_of_tracks)
            }
        elif i == 1:
            dp[f[0]] = {
                'label': f[1],
                'type': 'date',
                'required': True,
                'value': album.date
            }
        elif i in (2, 3, 4, 5, 11):
            dp[f[0]] = {
                'label': f[1],
                'type': 'text',
                'required': True if i == 3 else False,
                'size': 200 if f[3] > 200 else f[3],
                'value': format_td(album.catalog_number if i == 2 else (album.note if i == 11 else album.get_name(i))),
                'note': f' <span class="font80">(до {f[3]} символов)</span>'
            }
        elif i in (8, 9, 10):
            dp[f[0]] = {
                'label': f[1],
                'type': 'selOpt',
                'required': True if i == 8 else False,
                'fields': '*',
                'table': f[2],
                'option': fields()[20][2],
                'selectedValue': album.media_format if i == 8 else (album.label if i == 9 else album.manufacturer)
            }
    templ_name = f'edit.html'
    context = {
        'caption': f'Правка {fields()[5][1].lower()}а',
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_edit': Form(request, dp, sub_cancel_value='Отмена')
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefEAl', set_ref, 900)
        return response
    return render(request, templ_name, context)


def form_edit_album(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefEAl' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 13, 14, 2, 3, 4, 15, 16, 17, 18, 19, 12])
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (2, 3, 4, 12, 14))):
                edit_album(cf, request.POST, _id)
                return redirect_(request, 'MrefEAl', fields()[5][2])
            return show(request, cf, set_ref, _id, err)
        elif 'cancel' in request.POST:
            return redirect_(request, 'MrefEAl', fields()[5][2])
    return show(request, cf, set_ref, _id)
