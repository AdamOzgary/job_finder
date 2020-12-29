from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View


from .forms import CreateUserForm, LoginUserForm
from .utils import AuthenticateViewMixin


def show_base(request):
    return render(request, 'jf/index.html')


@login_required
def logout_req(request):
    logout(request)
    return redirect(reverse('home'))


class CreateUser(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'jf/sign_up.html', context={'form': form})
    
    def post(self, request):
        bound_form = CreateUserForm(request.POST)

        if bound_form.is_valid():
            bound_form.save()
            username = bound_form.cleaned_data.get('username')
            password = bound_form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=password)
            login(request, user)
            return show_base(request)
        return render(request, 'jf/sign_up.html', context={'form': bound_form})


class AuthenticateUser(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'jf/sign_up.html', context={'form': form})

    def post(self, request): 
        bound_form = LoginUserForm(request.POST)

        if bound_form.is_valid():

            username = bound_form.cleaned_data.get('username')
            password = bound_form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print('актив')
                    return show_base(request)
            else:
                error = 'Please enter a correct username and password.\
                    Note that both fields may be case-sensitive.'
                return render(request, 'jf/sign_up.html', context={
                        'form': bound_form,
                        'error': error
                })
        print("Не валидная форма", bound_form)
        return render(request, 'jf/sign_up.html', context={'form': bound_form})
