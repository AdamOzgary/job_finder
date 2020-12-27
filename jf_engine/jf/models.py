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

    #владелец
    owner = m.OneToOneField(User, m.CASCADE, related_name='organizations')


class Recruiter(m.Model): 
    """HR-менеджеры"""
    description = m.CharField(max_length=50)
    reg_date = m.DateTimeField(auto_now_add=True)

    # пользователем
    user = m.OneToOneField(User, m.CASCADE, pk=True)
    # одна огранизация - много рекрутеров
    organization = m.ForeignKey(Organization, m.CASCADE, related_name="recruiters")


class Vacancy(m.Model):
    """Вакансия"""
    title = m.TextField(db_index=True)
    description = m.TextField()
    post_date = m.DateTimeField(auto_now_add=True)

    # одна категория - много вакансий
    category = m.ForeignKey(Category, m.CASCADE, related_name='vacanсies')
    # много вакансий - много навыков
    key_skills = m.ManyToManyField(KeySkills, "vacancies")
    # одна категория - много вакансий
    organization = m.ForeignKey(Organization, m.CASCADE)