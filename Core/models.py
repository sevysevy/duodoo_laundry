from django.db import models
from django.utils import timezone
from datetime import date

from FinanceManagement.models import Expense
from OrderManagement.models import Order, Payment
from UserManagement.models import Agency, UserProfile

class SaleSession(models.Model):
    SESSION_STATUS = [
        ('open', 'Ouverte'),  # Open
        ('closed', 'Fermée'),  # Closed
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    agency  = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=SESSION_STATUS, default='open')
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    opening_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    added_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    removed_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    closing_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def close_session(self):
        """Close the session, calculate totals for sales, payments, and expenses."""
        self.end_time = timezone.now()
        self.status = 'closed'
        self.total_sales = self.calculate_total_sales()
        self.total_payments = self.calculate_total_payments()
        self.total_expenses = self.calculate_total_expenses()
        self.save()


    def add_fund(self, amount):
        self.added_fund += amount
        self.save()

    def add_removed_fund(self, amount):
        self.removed_fund += amount
        self.save()


    def calculate_closing_fund(self):
        """Calculate the closing fund based on opening fund, added fund, and removed fund."""
        return self.opening_fund + self.added_fund - self.removed_fund

    def calculate_total_sales(self):
        """Calculate the total amount from sales associated with this session."""
        exclude = ['draft']
        return Order.objects.filter(session=self  ).exclude(status__in = exclude).aggregate(total=models.Sum('total'))['total'] or 0.00

    def calculate_total_payments(self):
        """Calculate the total amount from payments associated with this session."""
        return Payment.objects.filter(session=self).aggregate(total=models.Sum('amount'))['total'] or 0.00

    def calculate_total_expenses(self):
        """Calculate the total amount from expenses associated with this session."""
        return Expense.objects.filter(session=self).aggregate(total=models.Sum('amount'))['total'] or 0.00

    @classmethod
    def check_open_session(cls):
        """Check if there's an open session for the user that needs closing."""
        open_session = SaleSession.objects.filter(status='open').first()
        if open_session:
            # The session is from a previous day and needs to be closed
            return open_session
        return None

    def __str__(self):
        return f"SaleSession(id={self.id}, user={self.user.username}, status={self.status})"
