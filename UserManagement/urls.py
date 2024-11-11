# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Role URLs
    path('roles/', views.role_list, name='role_list'),
    path('roles/<int:role_id>/', views.role_detail, name='role_detail'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/update/<int:pk>/', views.role_update, name='role_update'),
    path('roles/delete/<int:pk>/', views.role_delete, name='role_delete'),

    # UserProfile URLs
    path('profiles/', views.userprofile_list, name='userprofile_list'),
    path('profiles/create/', views.userprofile_create, name='userprofile_create'),
    path('profiles/update/<int:pk>/', views.userprofile_update, name='userprofile_update'),
    path('profiles/delete/<int:pk>/', views.userprofile_delete, name='userprofile_delete'),
    path('profiles/<int:pk>/', views.userprofile_detail, name='userprofile_detail'),


    path('customers/', views.customer_list, name='customer_list'),

    path('login', views.Login.as_view(redirect_authenticated_user = True) , name='login'),
    path('logout', views.custom_logout , name='logout'),

    path('create-user', views.create_user , name='create-user'),
    path('create-super-user', views.create_super_user , name='create-super-user'),

    path('agencies/', views.agency_list, name='agency_list'),
    path('agencies/create/', views.agency_create, name='agency_create'),
    path('agencies/update/<int:pk>/', views.agency_update, name='agency_update'),
    path('agencies/delete/<int:pk>/', views.agency_delete, name='agency_delete'),
]
