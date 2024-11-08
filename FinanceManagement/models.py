from django.db import models
from decimal import Decimal
from UserManagement.models import UserProfile

# Create your models here.

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Espèces'),
        ('bank_transfer', 'Virement bancaire')
    ]
    
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total expense amount
    date = models.DateField()
    session = models.ForeignKey('Core.SaleSession', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True , related_name = 'expenses_created')  # Assuming User is the staff model
    partner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True , related_name = 'expenses')  # New field
    confirm = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
    def confirm(self):
        self.session.add_removed_fund(Decimal(self.amount))



class ExpensePayment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Espèces'),
        ('bank_transfer', 'Virement bancaire')
    ]

    expense = models.ForeignKey('Expense', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    received_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Payment de {self.amount} le {self.payment_date}"

