from django.urls import path
from .views import login, change_password, create_user, account, cancel, transfers

urlpatterns = [
    path('', login, name='login'),
    path('cambiarContraseña/', change_password, name='change_password'),
    path('nuevoUsuario/', create_user, name='signup'),
    path('cuenta/<int:account>', account, name='account'),
    path('cuenta/<int:account>/cancelar/', cancel, name='cancel_account'),
    path('cuenta/<int:account>/transferencias/', transfers, name='transfers'),
]
