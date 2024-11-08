from django.db import models

from UserManagement.models import UserProfile

# Create your models here.

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total expense amount
    date = models.DateField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True , related_name = 'expenses_created')  # Assuming User is the staff model
    partner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True , related_name = 'expenses')  # New field

    def __str__(self):
        return f"{self.category} - {self.amount}"
    @property
    def total_paid(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def balance_due(self):
        return self.amount - self.total_paid

    def __str__(self):
        return f"{self.category} - {self.amount}"



class ExpensePayment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Espèces'),
        ('bank_transfer', 'Virement bancaire')
    ]

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    received_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Payment de {self.amount} le {self.payment_date}"

