from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

# view to render the login page
def login(request):

    return render(request, 'login.html')