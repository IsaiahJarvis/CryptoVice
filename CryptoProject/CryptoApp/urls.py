from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketcaptool, name='marketcaptool'),
    path('call-python/', views.get_info_filter, name='get_info_filter'),
    path('check_task_status/<str:task_id>/', views.check_task_status, name='check_task_status')
]
