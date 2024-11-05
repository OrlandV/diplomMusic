from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .edit import edit_track
from .redirect_ import redirect_
from .Track import Track
from .album_query import get_album_query
from .author_query import get_author_query
from .format_td import format_td
from .show_errors import show_errors
from .classes import Form


def show(request, cf: list, set_ref: str | bool, _id: int | None = None, err: list | None = None) -> HttpResponse:
    def note(text: str) -> str:
        return f' <span class="font80">({text})</span>'

    alf = cur_fields([0, 2, 3, 4, 13, 14, 17, 18])
    auf = cur_fields([0, 21, 22])
    track = Track(cf, _id)
    table_author = get_author_query(auf, 1)
    option_author = get_author_query(auf, 4)
    dp = {}
    for i, f in enumerate(cf):
        if i in (0, 6):
            dp[f[0]] = {
                'label': f[1],
                'type': 'number',
                'disabled': False if i else True,
                'value': track.number_in_album if i else _id
            }
            if i:
                dp[f[0]].update({'min': 1, 'step': 1})
        elif i in (1, 5, 8, 9, 10, 11):
            dp[f[0]] = {
                'label': f[1],
                'type': 'selOpt',
                'multiple': False if i == 5 else True,
                'required': True if i == 5 else False,
                'size': 0 if i == 5 else 6,
                'fields': '*',
                'table': get_album_query(alf, 2) if i == 5 else (f[2] if i == 11 else table_author),
                'option': get_album_query(alf, 3) if i == 5 else
                    ([alf[1][2], alf[2][2], alf[3][2], alf[4][2]] if i == 11 else option_author),
                'sort': fields()[3][2] if i == 11 else fields()[22][2],
                'selectedId': track.get_album_id() if i == 5 else
                    (track.get_ost_from_id() if i == 11 else track.get_author_id(i)),
                'optionWidth': 198,
                'note': '' if i == 5 else note('множественный выбор с помощью CTRL и SHIFT')
            }
            if i not in (5, 11):
                dp[f[0]]['separator'] = ' / '
        elif i in (2, 3, 4, 12):
            dp[f[0]] = {
                'label': f[1],
                'type': 'text',
                'required': True if i == 2 else False,
                'size': 200 if f[3] > 200 else f[3],
                'value': format_td(track.notes if i == 12 else track.get_name(i), False),
                'note': note(f'до {f[3]} символов')
            }
        elif i == 7:
            dp[f[0]] = {
                'label': f[1],
                'type': 'time',
                'required': True,
                'step': 1,
                'value': track.duration
            }
    templ_name = f'edit.html'
    context = {
        'caption': f'Правка {fields()[23][1].lower()}а',
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_edit': Form(request, dp, sub_cancel_value='Отмена')
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefET', set_ref, 900)
        return response
    return render(request, templ_name, context)


def form_edit_track(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefET' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields(list(range(13)))
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (2, 3, 4, 12))):
                edit_track(cf, request.POST, _id)
                return redirect_(request, 'MrefET', fields()[23][2])
            return show(request, cf, set_ref, _id, err)
        elif 'cancel' in request.POST:
            return redirect_(request, 'MrefET', fields()[23][2])
    return show(request, cf, set_ref, _id)
