from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name="login"),
    path('recup_pass/', views.recup_pass, name="recup_pass"),
    path('home/', views.home, name="home"),
    path('registro/', views.registro, name="registro"),
    path('editar/<str:clave_docente>/', views.edicion_docente, name='docente_edit'),
    path('proyectos/', views.lista_proyectos, name="lista_proyectos"),
    path('nuevo_proyecto/', views.agregar_proyecto_general, name="agregar_proyecto"),
    path('proyectos/editar/<str:pk>/', views.editar_proyecto, name="editar_proyecto"),
    path('proyectos/eliminar/<str:pk>/', views.eliminar_proyecto, name="eliminar_proyecto"),
] 