from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .edit_ost_from import edit_ost_from
from .redirect_ import redirect_
from .OSTFrom import OSTFrom
from .format_td import format_td
from .show_errors import show_errors
from .classes import Form


def show(request, cf: list, set_ref: str | bool, _id: int | None = None, err: list | None = None) -> HttpResponse:
    ost = OSTFrom(cf, _id)
    dp = {}
    for i, f in enumerate(cf):
        if i == 0:
            dp[f[0]] = {
                'label': f[1],
                'type': 'number',
                'disabled': True,
                'value': str(_id)
            }
        elif i == 4:
            dp[f[0]] = {
                'label': f[1],
                'type': 'date',
                'required': True,
                'value': ost.date
            }
        else:
            dp[f[0]] = {
                'label': f[1],
                'type': 'text',
                'required': True if i == 1 else False,
                'size': 200 if f[3] > 200 else f[3],
                'value': format_td(ost.get_name(i)),
                'note': f' <span class="font80">(до {f[3]} символов)</span>'
            }
    templ_name = f'edit.html'
    context = {
        'caption': f'Правка в «{fields()[11][1]}»',
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_edit': Form(request, dp, sub_cancel_value='Отмена')
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefEO', set_ref, 900)
        return response
    return render(request, templ_name, context)


def form_edit_ost_from(request, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefEO' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 2, 3, 4, 13])
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (2, 3, 4))):
                edit_ost_from(cf, request.POST, _id)
                return redirect_(request, 'MrefEO', fields()[11][2])
            return show(request, cf, set_ref, _id, err)
        elif 'cancel' in request.POST:
            return redirect_(request, 'MrefEO', fields()[11][2])
    return show(request, cf, set_ref, _id)
