from django.urls import path
from account.views import CustomUserLoginAPI, CustomUserRegistrationAPI, CustomUserDetailsAPI, CinemaOccupancyView

urlpatterns = [
    path("sign-up/", CustomUserRegistrationAPI.as_view(), name="custom-user-sign-up"),
    path("login/", CustomUserLoginAPI.as_view(), name="custom-user-login"),
    path("user/<int:id>/", CustomUserDetailsAPI.as_view(), name="custom-user-details-api"),
    path("occupancy", CinemaOccupancyView.as_view(), name="cinema-occupancy-view"),
]
