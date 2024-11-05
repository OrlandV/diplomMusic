from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .edit import edit_author
from .redirect_ import redirect_
from .Author import Author
from .format_td import format_td
from .show_errors import show_errors
from .classes import Form


def show(request, cf: list, set_ref: str | bool, _id: int | None = None, err: list | None = None) -> HttpResponse:
    a = Author(cf, 1, aid=_id)
    dp = {}
    for i, f in enumerate(cf):
        if i > 0:
            dp[f[0]] = {
                'label': f[1],
                'type': 'text',
                'required': True if i == 1 else False,
                'size': f[3],
                'value': format_td(a.get_name(i)),
                'note': f' <span class="font80">(до {f[3]} символов)</span>'
            }
        else:
            dp[f[0]] = {
                'label': f[1],
                'type': 'number',
                'disabled': True,
                'value': str(_id)
            }
    templ_name = f'edit.html'
    context = {
        'caption': f'Правка {fields()[24][1].lower()}а',
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_edit': Form(request, dp, sub_cancel_value='Отмена')
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefEA', set_ref, 900)
        return response
    return render(request, templ_name, context)


def form_edit_author(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefEA' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 21, 22])
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (21, 22))):
                edit_author(cf, request.POST, _id)
                return redirect_(request, 'MrefEA', fields()[24][2])
            return show(request, cf, set_ref, _id, err)
        elif 'cancel' in request.POST:
            return redirect_(request, 'MrefEA', fields()[24][2])
    return show(request, cf, set_ref, _id)
