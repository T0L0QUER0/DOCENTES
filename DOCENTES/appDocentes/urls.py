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
    path('nuevo_proyecto/', views.agregar_proyecto, name="agregar_proyecto"),
    path('proyectos/editar/<str:pk>/', views.editar_proyecto, name="editar_proyecto"),
    path('proyectos/eliminar/<str:pk>/', views.eliminar_proyecto, name="eliminar_proyecto"),
    path('docente/<str:clave_docente>/cedulas/', views.lista_cedulas, name='lista_cedulas'),
    path('docente/<str:clave_docente>/cedulas/agregar/', views.agregar_cedula, name='agregar_cedula'),
    path('docente/<str:clave_docente>/cedulas/editar/<str:id_cedula>/', views.editar_cedula, name='editar_cedula'),
    path('docente/<str:clave_docente>/cedulas/eliminar/<str:id_cedula>/', views.eliminar_cedula, name='eliminar_cedula'),
    #Recuperacion de contraseñas django
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html' ), name='password_reset'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', html_email_template_name='registration/password_reset_email.html', subject_template_name='registration/password_reset_subject.txt'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_edit.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
] 