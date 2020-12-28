from django.urls import path

from .views import show_base, CreateUser

urlpatterns = [
    path('', show_base),
    path('sign-up', CreateUser.as_view(), name='sign_up')
]