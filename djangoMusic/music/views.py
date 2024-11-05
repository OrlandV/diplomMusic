from .fields import fields
from .search import search
from .form_add_track import form_add_track
from .form_add_author import form_add_author
from .form_add_album import form_add_album
from .form_add_ost_from import form_add_ost_from
from .form_add_name import form_add_name
from .form_edit_track import form_edit_track
from .form_edit_author import form_edit_author
from .form_edit_album import form_edit_album
from .form_edit_ost_from import form_edit_ost_from
from .form_edit_name import form_edit_name
from .form_del_track import form_del_track
from .form_del_author import form_del_author
from .form_del_album import form_del_album
from .form_del_ost_from import form_del_ost_from
from .form_del_name import form_del_name


def main(request):
    return search(request)


def add_table(request, table):
    if table == fields()[23][2]:
        return form_add_track(request)
    elif table == fields()[24][2]:
        return form_add_author(request)
    elif table == fields()[5][2]:
        return form_add_album(request)
    elif table == fields()[11][2]:
        return form_add_ost_from(request)
    elif table == fields()[17][2]:
        return form_add_name(request, 17)
    elif table == fields()[18][2]:
        return form_add_name(request, 18)
    elif table == fields()[19][2]:
        return form_add_name(request, 19)


def edit_table(request, table, _id):
    if table == fields()[23][2]:
        return form_edit_track(request, _id)
    elif table == fields()[24][2]:
        return form_edit_author(request, _id)
    elif table == fields()[5][2]:
        return form_edit_album(request, _id)
    elif table == fields()[11][2]:
        return form_edit_ost_from(request, _id)
    elif table == fields()[17][2]:
        return form_edit_name(request, 17, _id)
    elif table == fields()[18][2]:
        return form_edit_name(request, 18, _id)
    elif table == fields()[19][2]:
        return form_edit_name(request, 19, _id)


def del_table(request, table, _id):
    if table == fields()[23][2]:
        return form_del_track(request, _id)
    elif table == fields()[24][2]:
        return form_del_author(request, _id)
    elif table == fields()[5][2]:
        return form_del_album(request, _id)
    elif table == fields()[11][2]:
        return form_del_ost_from(request, _id)
    elif table == fields()[17][2]:
        return form_del_name(request, 17, _id)
    elif table == fields()[18][2]:
        return form_del_name(request, 18, _id)
    elif table == fields()[19][2]:
        return form_del_name(request, 19, _id)
