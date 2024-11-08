# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/update/<int:pk>/', views.service_update, name='service_update'),
    path('services/delete/<int:pk>/', views.service_delete, name='service_delete'),

    path('itemtypes/', views.itemtype_list, name='itemtype_list'),
    path('itemtypes/new/', views.itemtype_create, name='itemtype_create'),
    path('itemtypes/<int:pk>/edit/', views.itemtype_update, name='itemtype_update'),
    path('itemtypes/<int:pk>/delete/', views.itemtype_delete, name='itemtype_delete'),


    path('itemcharacteristics/', views.itemcharacteristic_list, name='itemcharacteristic_list'),
    path('itemcharacteristics/new/', views.itemcharacteristic_create, name='itemcharacteristic_create'),
    path('itemcharacteristics/<int:pk>/edit/', views.itemcharacteristic_update, name='itemcharacteristic_update'),
    path('itemcharacteristics/<int:pk>/delete/', views.itemcharacteristic_delete, name='itemcharacteristic_delete'),

    path('itemcategories/', views.itemcategory_list, name='itemcategory_list'),
    path('itemcategories/new/', views.itemcategory_create, name='itemcategory_create'),
    path('itemcategories/<int:pk>/edit/', views.itemcategory_update, name='itemcategory_update'),
    path('itemcategories/<int:pk>/delete/', views.itemcategory_delete, name='itemcategory_delete'),
    path('itemcategories/<int:pk>/', views.itemcategory_detail, name='itemcategory_detail'),


    path('pricelist/', views.pricelist_list, name='pricelist_list'),
    path('pricelist/new/', views.pricelist_create, name='pricelist_create'),
    path('pricelist/<int:pk>/edit/', views.pricelist_update, name='pricelist_update'),
    path('pricelist/<int:pk>/delete/', views.pricelist_delete, name='pricelist_delete'),
    path('get_item_types_by_category/<int:category_id>/', views.get_item_types_by_category, name='get_item_types_by_category'),

]
