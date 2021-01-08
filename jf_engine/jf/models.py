from django.db import models as m
from django.contrib.auth import get_user_model


User = get_user_model()


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
    site_link = m.URLField(unique=True)
    slug = m.SlugField(unique=True, max_length=20)
    description = m.TextField()
    reg_date = m.DateTimeField(auto_now_add=True)

    owner = m.OneToOneField(User,
        on_delete=m.CASCADE,
        related_name='organizations'
    )

class Recruiter(m.Model): 
    """HR-менеджеры"""
    description = m.TextField()
    user = m.OneToOneField(User,
        on_delete=m.CASCADE,
        primary_key=True
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
        related_name="vacancies"
    )
    organization = m.ForeignKey(Organization,
        on_delete=m.CASCADE,
        related_name="vacancies"
    )


class Resume(m.Model):
    """Резюме"""
    title = m.TextField(db_index=True)
    description = m.TextField(blank=True)
    post_date = m.DateTimeField(auto_now_add=True)
    

    user = m.ForeignKey(User,
        on_delete=m.CASCADE,
        related_name="resumes"
    )
    category = m.ForeignKey(Category, 
        on_delete=m.CASCADE,
        related_name='resumes'     
    )
    key_skills = m.ManyToManyField(KeySkills,
        related_name="resumes"
    )