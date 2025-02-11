from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketcaptool, name='marketcaptool'),
    path('call-python/', views.get_holders_quick, name='get_holders_quick'),
    path('call-python-filter/', views.get_holders_filter, name='get_holders_filter'),
]
