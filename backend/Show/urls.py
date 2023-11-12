from django.urls import path
from .views import show_list, ShowCreateView, ShowUpdateView, ShowDeleteView

urlpatterns = [
    path('shows/', show_list, name='show_list'),
    path('shows/new/', ShowCreateView.as_view(), name='show_create'),
    path('shows/<uuid:pk>/edit/', ShowUpdateView.as_view(), name='show_edit'),
    path('shows/<uuid:pk>/delete/', ShowDeleteView.as_view(), name='show_delete'),
]
