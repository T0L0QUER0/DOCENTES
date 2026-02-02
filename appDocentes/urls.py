from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import PasswordReset


urlpatterns = [
    path('', views.login_view, name="login"),
    path('logout/', views.logout_usuario, name='logout'),
    path('recup_pass/', views.recup_pass, name="recup_pass"),
    path('home/', views.home, name="home"),
    path('registro/', views.registro, name="registro"),
    path('editar/<str:clave_docente>/', views.edicion_docente, name='docente_edit'),
    path('proyectos/', views.lista_proyectos, name="lista_proyectos"),
    path('nuevo_proyecto/', views.agregar_proyecto_general, name="agregar_proyecto"),
    path('proyectos/editar/<str:pk>/', views.editar_proyecto, name="editar_proyecto"),
    path('proyectos/eliminar/<str:pk>/', views.eliminar_proyecto, name="eliminar_proyecto"),
    #Recuperacion de contraseñas django
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html' ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_edit.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
] 