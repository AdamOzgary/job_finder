from django import forms as f
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from .models import (
        KeySkills,
        Category,
        Vacancy,
        Organization,
        Recruiter,
        Resume
)

User = get_user_model()
form_template =  'jf/form_base.html'


class CreateUserForm(f.ModelForm):
    submit_btn = 'Sign Up'
    page_title = 'Registration'

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = f.CharField(
        label=_("Password"),
        strip=False,
        widget=f.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = f.CharField(
        label=_("Password confirmation"),
        widget=f.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        field_classes = {'username': UsernameField}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginUserForm(f.Form):
    submit_btn = 'Sign In'
    page_title = 'Login'

    error_messages = None
    username = UsernameField()
    password = f.CharField(widget=f.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not User.objects.filter(username=username).count():
            raise ValidationError("A user with this username does not exist")
        
        return username


class OrganizationForm(f.ModelForm):
    submit_btn = 'Add'
    page_title = 'Add Organization'

    class Meta:
        model = Organization
        fields = ['name', 'site_link', 'description']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        if self.request.user.organization is not None:
            raise ValidationError(
                f'You have organization {self.request.user.organization.slug}'
            )
        super().__init__(*args, **kwargs)
        
    def clean_name(self):
        new_name = self.cleaned_data.get('name').lower()
        if new_name == 'create':
            raise ValidationError('Name may not be "Create".')
        if Organization.objects.filter(name__iexact=new_name).count():
            raise ValidationError(
                    'There is already an organization with the same name')
        return self.cleaned_data.get('name')

    def save(self):
        new_org = Organization.objects.create(
            name = self.cleaned_data.get('name'),
            site_link = self.cleaned_data.get('site_link'),
            description = self.cleaned_data.get('description'),
            owner = self.request.user
        )
        return new_org


class KeySkillsForm(f.ModelForm):
    submit_btn = 'Add'
    page_title = 'New key skill'

    class Meta:
        model = KeySkills
        fields = ['title', 'slug']

    def clean_slug(self):
        new_slug = self.cleaned_data.get('slug').lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create".')
        if KeySkills.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(\
                    f'Slug must be unique. We have "{new_slug}" slug')
        return new_slug

    def save(self):
        new_key_skill = KeySkills.objects.create(
            title=self.cleaned_data.get('title'),
            slug=self.cleaned_data.get('slug')
        )
        return new_key_skill


class CategoryForm(f.ModelForm):
    submit_btn = 'Add'
    page_title = 'New category'

    class Meta:
        model = Category
        fields = ['title', 'slug']
    
    def clean_slug(self):
        new_slug = self.cleaned_data.get('slug').lower()
        
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create".')
        if Category.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(\
                    f'Slug must be unique. We have "{new_slug}" slug')
        return new_slug

    def save(self):
        new_category = Category.objects.create(
            title=self.cleaned_data.get('title'),
            slug=self.cleaned_data.get('slug')
        )
        return new_category


class VacancyForm(f.ModelForm):
    submit_btn = 'Post'
    page_title = 'New vacancy'

    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'organization', 'category', 'key_skills']


class ResumeForm(f.ModelForm):
    submit_btn = 'Post'
    page_title = 'New resume'

    class Meta:
        model = Resume
        fields = ['title', 'key_skills', 'description']


class RecruiterForm(CreateUserForm):
    submit_btn = 'Create'
    page_title = 'New recruter'

    description = f.CharField()
    
    def save(self, organization):
        user = super().save()
        new_recruter = Recruiter.objects.create(
            user=user, 
            description=self.cleaned_data.get('descritpion'),
            organization=organization
        )
