from django.urls import path
from .views import login, change_password

urlpatterns = [
    path('', login, name='login'),
    path('cambiar contraseña/', change_password, name='change_password'),
]
