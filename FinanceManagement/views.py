from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy

from UserManagement.models import UserProfile
from .models import Expense, ExpenseCategory
from django.http import HttpResponseRedirect


class ExpenseCategoryListView(View):
    def get(self, request):
        categories = ExpenseCategory.objects.all()
        return render(request, 'expense_category_list.html', {'categories': categories})

class ExpenseCategoryCreateView(View):
    def get(self, request):
        return render(request, 'expense_category_form.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validation
        if not name:
            return render(request, 'expense_category_form.html', {
                'error': 'Name is required',
                'name': name,
                'description': description
            })

        # Save the new expense category
        ExpenseCategory.objects.create(name=name, description=description)
        return redirect('expense_category_list')


class ExpenseCategoryUpdateView(View):
    def get(self, request, pk):
        category = get_object_or_404(ExpenseCategory, pk=pk)
        return render(request, 'expense_category_update.html', {
            'name': category.name,
            'description': category.description,
            'category': category
        })

    def post(self, request, pk):
        category = get_object_or_404(ExpenseCategory, pk=pk)
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validation
        if not name:
            return render(request, 'expense_category_update.html', {
                'error': 'Name is required',
                'name': name,
                'description': description,
                'category': category
            })

        # Update the category
        category.name = name
        category.description = description
        category.save()
        return redirect('expense_category_list')


class ExpenseCategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(ExpenseCategory, pk=pk)
        return render(request, 'expense_category_confirm_delete.html', {'category': category})

    def post(self, request, pk):
        category = get_object_or_404(ExpenseCategory, pk=pk)
        category.delete()
        return redirect('expense_category_list')



class ExpenseListView(View):
    def get(self, request):
        expenses = Expense.objects.all()
        return render(request, 'expense_list.html', {'expenses': expenses})


class ExpenseCreateView(View):
    def get(self, request):
        categories = ExpenseCategory.objects.all()
        partners = UserProfile.objects.all().order_by('fullName')
        return render(request, 'expense_form.html', {
            'categories': categories,
            'partners': partners,
            'title': 'Ajouter une nouvelle dépense',
            'button_text': 'Enregistrer'
        })

    def post(self, request):
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        partner_id = request.POST.get('partner')

        # Validation
        if not category_id or not amount or not date:
            partners = UserProfile.objects.all().order_by('fullName')
            categories = ExpenseCategory.objects.all()
            return render(request, 'expense_form.html', {
                'error': 'Tous les champs requis ne sont pas remplis',
                'categories': categories,
                'partners': partners,
                'title': 'Ajouter une nouvelle dépense',
                'button_text': 'Enregistrer',
                'description': description,
                'amount': amount,
                'date': date,
                'partner_id': partner_id,
            })

        # Save the new expense
        category = get_object_or_404(ExpenseCategory, pk=category_id)
        partner = UserProfile.objects.get(pk=partner_id) if partner_id else None
        Expense.objects.create(
            category=category,
            description=description,
            amount=amount,
            date=date,
            partner=partner
        )
        return redirect('expense_list')



class ExpenseUpdateView(View):
    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        categories = ExpenseCategory.objects.all()
        partners = UserProfile.objects.all().order_by('fullName')
        return render(request, 'expense_form.html', {
            'categories': categories,
            'partners': partners,
            'expense': expense,
            'title': 'Modifier la dépense',
            'button_text': 'Mettre à jour'
        })

    def post(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        partner_id = request.POST.get('partner')

        # Validation
        if not category_id or not amount or not date:
            categories = ExpenseCategory.objects.all()
            partners = UserProfile.objects.all().order_by('fullName')
            return render(request, 'expense_form.html', {
                'error': 'Tous les champs requis ne sont pas remplis',
                'categories': categories,
                'expense': expense,
                'partners': partners,
                'title': 'Modifier la dépense',
                'button_text': 'Mettre à jour',
                'description': description,
                'amount': amount,
                'date': date,
                'partner_id': partner_id,
            })

        # Update the expense
        category = get_object_or_404(ExpenseCategory, pk=category_id)
        expense.category = category
        expense.description = description
        expense.amount = amount
        expense.date = date
        expense.save()
        return redirect('expense_list')


class ExpenseDeleteView(View):
    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        return render(request, 'expense_confirm_delete.html', {'expense': expense})

    def post(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return redirect('expense_list')
