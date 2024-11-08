# forms.py
from django import forms
from .models import Role, UserProfile

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name',  'desc_role']
        labels = {
            'name': 'Nom du rôle',       # Custom label for 'name' field
            'desc_role': 'Description',  # Custom label for 'desc_role' field
        }

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Entrer de nouveau le mot de passe")
    class Meta:
        model = UserProfile
        fields = ['firstName', 'lastName',  'email', 'phone',  'role']
        labels = {
            'firstName': 'Prénom',      # Custom label for 'firstName' field
            'lastName': 'Nom',          # Custom label for 'lastName' field
            'email': 'Adresse e-mail',  # Custom label for 'email' field
            'phone': 'Numéro de téléphone',  # Custom label for 'phone' field
            'role': 'Rôle',             # Custom label for 'role' field
        }
