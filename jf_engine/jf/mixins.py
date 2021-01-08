from abc import abstractmethod, ABC

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import AccessMixin
from django import forms as f
from django.shortcuts import render, redirect, reverse

from .forms import form_template

class ViewMixin(ABC):
    form: f.Form
    redirect_to = 'home'
    def get(self, request):
        form = self.form()
        return render(request, form_template, context={'form': form})

    def post(self, request):
        bound_form = self.form(request.POST)

        if bound_form.is_valid():
            return self.if_valid(bound_form, request)
        
        return render(request, form_template, context={'form': bound_form})
    
    @abstractmethod
    def if_valid(self, form, request): ...


class FormSaveViewMixin(ViewMixin):
    def if_valid(self, form, request):
        form.save()
        return redirect(reverse(self.redirect_to))
        

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is admin"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)