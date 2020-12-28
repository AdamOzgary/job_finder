from django.db import models as m
from django.contrib.auth.models import User


class KeySkills(m.Model):
    """Ключевые навыки аля теги"""
    title = m.CharField(max_length=30, db_index=True)
    slug = m.SlugField(max_length=20, unique=True)


class Category(m.Model):
    """Категории"""
    title = m.CharField(max_length=50, db_index=True)
    slug = m.SlugField(max_length=20, unique=True)


class Organization(m.Model):
    """Организация"""
    name = m.TextField(unique=True)
    site_link = m.URLField()
    description = m.TextField()
    reg_date = m.DateTimeField(auto_now_add=True)


    owner = m.ForeignKey(User,
            on_delete=m.CASCADE,
            related_name='organizations'
    )


class Recruiter(m.Model): 
    """HR-менеджеры"""
    description = m.CharField(max_length=50)
    reg_date = m.DateTimeField(auto_now_add=True)


    user = m.OneToOneField(User,
            on_delete=m.CASCADE,
            pk=True
    )
    organization = m.ForeignKey(Organization,
            m.CASCADE,
            related_name="recruiters"
    )


class Vacancy(m.Model):
    """Вакансия"""
    title = m.TextField(db_index=True)
    description = m.TextField()
    post_date = m.DateTimeField(auto_now_add=True)


    category = m.ForeignKey(Category,
            on_delete=m.CASCADE,
            related_name='vacanсies'
    )
    key_skills = m.ManyToManyField(KeySkills,
            on_delete=m.SET_NULL,
            related_name="vacancies"
    )
    organization = m.ForeignKey(Organization,
            on_delete=m.CASCADE,
            related_name="vacancies"
    )


class Resume(m.Model):
    """Резюме"""
    title = m.TextField(db_index=True)
    descrtiption = m.TextField(blank=True)
    post_date = m.DateTimeField(auto_now_add=True)
    

    user = m.ForeignKey(User,
            related_name="resumes"
    )
    key_skills = m.ManyToManyField(KeySkills,
            on_delete=m.SET_NULL,
            related_name="resumes"
    )