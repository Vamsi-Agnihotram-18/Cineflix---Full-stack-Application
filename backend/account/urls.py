from django.urls import path
from account.views import *


urlpatterns = [
    path('sign_up', sign_up, name='sign_up'),
    path('login', login, name='login'),
]