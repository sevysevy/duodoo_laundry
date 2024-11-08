# forms.py
from django import forms
from .models import ItemCategory, Service ,ItemType , ItemCharacteristic , PriceList

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']
        labels = {
            'name': 'Nom du Service',
            'description': 'Description',
        }


class ItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = ['name']
        labels = {
            'name': 'Nom du Type de vêtement'
        }

class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name', 'description']

class ItemCharacteristicForm(forms.ModelForm):
    class Meta:
        model = ItemCharacteristic
        fields = ['name']
        labels = {
            'name': 'Nom de la caracteristique'
        }


class PriceListForm(forms.ModelForm):
    class Meta:
        model = PriceList
        fields = ['service', 'item_type', 'item_characteristic', 'price']
        labels = {
            'service': 'Service',
            'item_type': 'Type de Vêtement',
            'item_characteristic': 'Caractéristique',
            'price': 'Prix',
        }
