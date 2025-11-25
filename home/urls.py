from django.contrib import admin
from django.urls import path
from . import views

# Función condicional que Django usará antes de acceder a las URLs de admin.
def restrict_admin_access(request):
    if not request.user.is_authenticated:
        return admin.site.urls(request) 
    if not request.user.is_superuser:
        return views.access_denied_view(request) 
    return admin.site.urls(request)

urlpatterns = [
    path('admin/', restrict_admin_access, name='admin'),
    path('', views.login_home, name='login_home'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('home/agregar_categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('run/', views.vista_agregar_tiempo, name='vista_agregar_tiempo'),
    path('contador/<int:pk>/', views.contador_tiempo, name='contador_tiempo'),
    path('muy_pronto/', views.Muy_Pronto, name='muy_pronto'),

]
