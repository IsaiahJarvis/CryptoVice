from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketcaptool, name='marketcaptool'),
    path('call-python/', views.user_submission, name='user_submission'),
]
