from django import forms
from .models import Order, Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'payment_date']

        labels = {
            'amount': 'Montant',
            'payment_method': 'Methode de paiement',
            'payment_date': 'Date de paiement',
        }



class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'status', 'total', 'balance']  # Include fields you want to allow updating

        # Optional: custom widgets or labels
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'client': 'Client',
            'status': 'Statut de la Commande',
            'total': 'Total Commande',
            'balance': 'Balance Restante',
        }