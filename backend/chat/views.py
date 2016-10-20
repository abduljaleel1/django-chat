from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

@login_required(login_url='login/')
def main(request):
    return HttpResponse('home')

def new_user(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('main')
        else:
            context = {
                'form': user
            }
            return render(request, 'new_user.html', context)
    else:
        context = {
            'form': UserCreationForm
        }
        return render(request, 'new_user.html', context)