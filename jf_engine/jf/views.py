from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.core.exceptions import ValidationError

from .forms import form_template
from .forms import CreateUserForm, LoginUserForm
from .forms import KeySkillsForm, CategoryForm
from .forms import OrganizationForm, RecruiterForm
from .forms import ResumeForm, VacancyForm
from .mixins import FormSaveViewMixin, ViewMixin, AdminRequiredMixin



def show_base(request):
    return render(request, 'jf/base_page.html')

@login_required
def logout_req(request):
    logout(request)
    return redirect(reverse('home'))


class CreateUserView(ViewMixin, View):
    form = CreateUserForm

    def if_valid(self, form, request):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse('home'))


class LoginUserView(ViewMixin, View):
    form = LoginUserForm

    def if_valid(self, form, request):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('home'))
            else: 
                # do something
                pass
        error = '''Please enter a correct username and password.'''
        return render(request,form_template, context={
                'form': form,
                'error': error
        })


class AddCategoryView(FormSaveViewMixin, View):
    form = CategoryForm


class AddKeySkillView(FormSaveViewMixin, View):
    form = KeySkillsForm


class AddOrganizationView(ViewMixin, View):
    form = OrganizationForm

    def if_valid(self, form, request):
        form.save(request)
        return redirect(reverse(self.redirect_to))


class AddRecruiterView(ViewMixin, View):
    form = RecruiterForm


class AddVacancyView(ViewMixin, View):
    form = VacancyForm


class AddResumeView(ViewMixin, View):
    form = ResumeForm