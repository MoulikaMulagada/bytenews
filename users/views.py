# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.http import HttpResponse

#def home(request):
#    return HttpResponse("Welcome to the Home Page")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can log in now.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
