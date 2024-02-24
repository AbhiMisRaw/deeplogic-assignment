from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('check-result/<str:result_id>', views.result_view, name='result')
]