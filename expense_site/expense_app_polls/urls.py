from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.login, name='login'),
    path('login_auth', views.login_auth, name='login_auth')
]