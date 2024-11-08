from django.shortcuts import redirect
from .get_param import get_param


def redirect_(request, cookie_name: str, table_name: str):
    re_params = get_param(request.GET)
    if cookie_name in request.COOKIES:
        response = redirect(request.COOKIES[cookie_name] + ('?' + re_params.urlencode() if len(re_params) else ''))
        response.delete_cookie(cookie_name)
        return response
    return redirect(f'/music/add/{table_name}/' + ('?' + re_params.urlencode() if len(re_params) else ''))
