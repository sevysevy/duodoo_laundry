# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Role URLs
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/update/', views.order_update, name='order_update'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('list/', views.order_list, name='order_list'),
    path('details/<int:pk>', views.order_detail, name='order_detail'),
    path("get_customers/", views.get_customers, name="get_customers"),
    path("add_client/", views.add_client, name="add_client"),
    path("get_item_types/", views.get_item_types, name="get_item_types"),
    path("get_price/", views.get_price, name="get_price"),
    path("get_characteristics_for_item_type/", views.get_characteristics_for_item_type, name="get_characteristics_for_item_type"),
    path("get_services_for_item_type/", views.get_sevice_for_item_type, name="get_sevice_for_item_type"),
    path('orders/<int:order_id>/payment/', views.register_payment, name='register_payment'),
    path('orders/<int:order_id>/create_batch/', views.create_batch, name='create_batch'),
    path('orders/create_batch_multy/', views.create_batch_multy, name='create_batch_multy'),
    path('batches/<str:batch_id>/', views.batch_detail, name='batch_detail'),
    path('batches/<str:batch_id>/update_status/', views.update_batch_status, name='update_batch_status'),
    path('batches/', views.batch_list, name='batch_list'),
    path('mark_items_as_delivered/', views.mark_items_as_delivered, name='mark_items_as_delivered'),
    path("<int:pk>/print" , views.order_receipt  , name="print_receipt"),
    path("<int:pk>/batch/print" , views.batch_receipt  , name="print_batch_receipt")
]
