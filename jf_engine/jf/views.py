from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from .forms import UserForm

def show_base(request):
    return render(request, 'jf/base_page.html')

class CreateUser(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'jf/sign_up.html', context={'form': form})
    
    def post(self, request):
        bound_form = UserForm(request.POST)

        if bound_form.is_valid():
            bound_form.save()
            username = bound_form.cleaned_data.get('username')
            password = bound_form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=password)
            login(request, user)
            return show_base(request)
        return render(request, 'jf/sign_up.html', context={'form': bound_form})


    