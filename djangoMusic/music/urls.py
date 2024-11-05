from django.urls import path
from .views import *

urlpatterns = [
    path('', main),
    path('add/<str:table>/', add_table),
    path('edit/<str:table>/<int:_id>/', edit_table),
    path('del/<str:table>/<int:_id>/', del_table)
]
