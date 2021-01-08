from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import KeySkills, Category, Organization, Recruiter, Vacancy, Resume 

# User = get_user_model()
admin.site.register(KeySkills)
admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(Recruiter)
admin.site.register(Vacancy)
admin.site.register(Resume)