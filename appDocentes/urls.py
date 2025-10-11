from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name="login"),
    path('recup_pass/', views.recup_pass, name="recup_pass"),
    path('home/', views.home, name="home"),
    path('registro/', views.registro, name="registro")
] 