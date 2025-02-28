from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import  authenticate, login as log_in, logout as log_out
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from account.models import User
from adminpanel.AuthBackend import AuthBackend

from django.db.models import Count
from django.db.models import Q, F
# Create your views here.

def Login(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, is_staff=True)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('admin_login')

        user = AuthBackend.authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, 'Invalid email or password')
            return redirect('admin_login')

        log_in(request, user)
        return redirect('product_list')

    return render(request, 'profile/login.html')

def Logout(request):
    log_out(request)
    return redirect('admin_login')


