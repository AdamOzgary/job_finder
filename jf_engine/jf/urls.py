from django.urls import path

from .views import show_base, logout_req
from .views import CreateUserView, LoginUserView
from .views import AddCategoryView, AddKeySkillView
from .views import AddOrganizationView, AddRecruiterView


urlpatterns = [
    path('', show_base, name='home'),
    path('sign-up', CreateUserView.as_view(), name='sign_up'),
    path('sign-in', LoginUserView.as_view(), name='sign_in'),
    path('key-skill/create', AddKeySkillView.as_view(), name='new_key_skill'),
    path('my-organization/create', AddOrganizationView.as_view(),
        name='new_organiztion'),
    path('my-organization/add-recruiter', AddRecruiterView.as_view()),
    path('logout', logout_req, name='logout')
]