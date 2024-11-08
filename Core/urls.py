# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Role URLs
    path('', views.home, name='home'),
]
