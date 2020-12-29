from django.urls import path

from .views import show_base, CreateUser, AuthenticateUser, logout_req

urlpatterns = [
    path('', show_base, name='home'),
    path('sign-up', CreateUser.as_view(), name='sign_up'),
    path('sign-in', AuthenticateUser.as_view(), name='sign_in'),
    path('logout',logout_req, name='logout')
]