from django.urls import path
from .views import login, change_password, create_user

urlpatterns = [
    path('', login, name='login'),
    path('cambiarContraseña/', change_password, name='change_password'),
    path('nuevoUsuario/', create_user, name='signup'),
]
