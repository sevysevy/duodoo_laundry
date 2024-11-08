from django.urls import path
from .views import (
    ExpenseCategoryListView,
    ExpenseCategoryCreateView,
    ExpenseCategoryUpdateView,
    ExpenseCategoryDeleteView,
    ExpenseListView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView,
)

urlpatterns = [
    path('expense-categories/', ExpenseCategoryListView.as_view(), name='expense_category_list'),
    path('expense-category/add/', ExpenseCategoryCreateView.as_view(), name='expense_category_create'),
    path('expense-category/<int:pk>/edit/', ExpenseCategoryUpdateView.as_view(), name='expense_category_update'),
    path('expense-category/<int:pk>/delete/', ExpenseCategoryDeleteView.as_view(), name='expense_category_delete'),

    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('expense/add/', ExpenseCreateView.as_view(), name='expense_create'),
    path('expense/<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
]
