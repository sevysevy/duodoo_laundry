# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Role URLs
    path('', views.home, name='home'),
    path('sale-session-list' , views.sale_session_list, name='sale_session_list'),
    path('sessions/open/', views.open_sale_session, name='open_sale_session'),
    path('sessions/close/<int:session_id>/', views.close_sale_session, name='close_sale_session'),
]
