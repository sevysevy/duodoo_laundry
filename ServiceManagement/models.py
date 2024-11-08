from django.db import models
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

        
class ItemType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name='item_types')

    def __str__(self):
        return self.name



class ItemCharacteristic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PriceList(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='price_entries')
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name='price_entries')
    item_characteristic = models.ForeignKey(ItemCharacteristic, on_delete=models.CASCADE, related_name='price_entries')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('service', 'item_type', 'item_characteristic')

    def __str__(self):
        return f"{self.service.name} - {self.item_type.name} - {self.item_characteristic.name} : {self.price}"
