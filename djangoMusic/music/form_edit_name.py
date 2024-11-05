from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .fields import *
from .validate_data import validate_data
from .edit_name import edit_name
from .redirect_ import redirect_
from .Name import Name
from .format_td import format_td
from .show_errors import show_errors
from .classes import Form


def show(request, cf: list, index: int, set_ref: str | bool, _id: int | None = None,
         err: list | None = None) -> HttpResponse:
    n = Name(cf, index, _id)
    dp = {}
    for i, f in enumerate(cf):
        if i:
            dp[f[0]] = {
                'label': f[1],
                'type': 'text',
                'required': True,
                'size': f[3],
                'value': format_td(n.name),
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
        'caption': f'Правка ' + (fields()[index][1][:-1].lower() + 'я' if index == 19 else
                                 fields()[index][1].lower() + 'а'),
        'err': show_errors(err, 'ОШИБКА в ведённых данных!') if err else None,
        'form_edit': Form(request, dp, sub_cancel_value='Отмена')
    }
    if set_ref:
        response = HttpResponse(render_to_string(templ_name, context, request))
        response.set_cookie('MrefEN', set_ref, 900)
        return response
    return render(request, templ_name, context)


def form_edit_name(request, index: int, _id: int):
    set_ref = False
    referrer = request.META.get('HTTP_REFERER')
    if 'MrefEN' not in request.COOKIES and referrer:
        set_ref = referrer
    cf = cur_fields([0, 20], True if index == 17 else False)
    if request.method == 'POST':
        if 'ok' in request.POST:
            if not (err := validate_data(request.POST, (20,))):
                edit_name(index, cf, request.POST, _id)
                return redirect_(request, 'MrefEN', fields()[index][2])
            return show(request, cf, index, set_ref, _id, err)
        elif 'cancel' in request.POST:
            return redirect_(request, 'MrefEN', fields()[index][2])
    return show(request, cf, index, set_ref, _id)
