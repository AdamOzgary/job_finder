from django.contrib.auth import authenticate, login
from django import forms as f
from django.shortcuts import render, redirect, reverse

class AuthenticateViewMixin:
    form: f.Form
    username_field_name = 'username'
    password_field_name = None
    template_name = None

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        bound_form = self.form(request.POST)

        if bound_form.is_valid():
            bound_form.save()
            username = bound_form.cleaned_data.get(self.username_field_name)
            password = bound_form.cleaned_data.get(self.password_field_name)
            
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('home'))
        return render(request, self.template_name, context={'form': bound_form})