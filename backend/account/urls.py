from django.urls import path
from account.views import UserLoginAPI, UserSignUpAPI


urlpatterns = [
    path("sign_up", UserSignUpAPI.as_view(), name="sign_up"),
    path("login", UserLoginAPI.as_view(), name="login"),
]
