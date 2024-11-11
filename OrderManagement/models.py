from django.db import models
from django.urls import reverse

from ServiceManagement.models import ItemCharacteristic, ItemType, Service
from UserManagement.models import Agency, UserProfile
from decimal import Decimal
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta

def default_two_days_later():
    return timezone.now().date() + timedelta(days=2)

class Batch(models.Model):
    BATCH_STATUS_CHOICES = [
        ('in_production', 'In Production'),
        ('completed', 'Completed')
    ]
    
    batch_id = models.CharField(max_length=255, null=True, editable=False)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=BATCH_STATUS_CHOICES, default="in_production")
    name = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.batch_id:
            # Generate the first four characters of the agency name
            prefix="PROD"
            if self.agency:
                prefix = f"PROD-{slugify(self.agency.name)[:4].upper()}"
            
            # Get the latest order for this agency and increment the numeric part
            last_batch = Batch.objects.all().order_by('-id').first()
            if last_batch and last_batch.batch_id and last_batch.batch_id.startswith(prefix):
                # Extract the numeric part and increment it
                last_number = int(last_batch.batch_id.split('-')[-1])
                new_number = f"{last_number + 1:04}"  # Format as a 4-digit number with leading zeros
            else:
                new_number = "0001"  # Start from 0001 if no previous order exists
            
            # Set the order_id with prefix and new incremental number
            self.batch_id = f"{prefix}-{new_number}"
        
        super().save(*args, **kwargs)

    def add_items_to_batch(self, order_item_ids):
        """
        Add items to this batch and set their status to 'production'.
        """
        order_items = OrderLineItem.objects.filter(id__in=order_item_ids)
        order_items.update(batch=self, status='production')
        for item in order_items:
            print(item.batch)
            print(item.id)
            item.order.update_status()  # Update order status based on new item status
            item.save()

    def complete_batch(self):
        """
        Mark the batch as completed and set all related items to 'complete'.
        """
        self.status = 'completed'
        self.save()
        self.items.update(status='completed')  # Update all items in this batch to 'complete'
        
        # Update related orders' statuses
        for item in self.items.all():
            print("updation order from batch")
            item.order.update_status()  # Ensure order status is updated

    def items_count(self):
        result=0
        for elm in self.items.all():

            result = result + elm.quantity 

        return result
    
    def receipt_url(self):
        return  reverse('print_batch_receipt' , args=[self.id])


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'Pending'),
        ('partial_production', 'Partial Production'),
        ('production', 'Production'),
        ('complete', 'Complete'),
        ('delivered', 'Delivered')
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('partial', 'Paiement partiel'),
        ('complete', 'Complet'),
    ]


    order_id = models.CharField(max_length=255, null=True, editable=False)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default="draft")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default="pending")
    session = models.ForeignKey('Core.SaleSession', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    ristourne = models.IntegerField(null=True)
    total = models.IntegerField()
    balance = models.IntegerField(null=True)
    delivery_date = models.DateField(null=True , default=default_two_days_later )



    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate the first four characters of the agency name
            prefix="CMD"
            if self.agency:
                prefix = slugify(self.agency.name)[:4].upper()
            
            # Get the latest order for this agency and increment the numeric part
            last_order = Order.objects.all().order_by('-id').first()
            if last_order and last_order.order_id and last_order.order_id.startswith(prefix):
                # Extract the numeric part and increment it
                last_number = int(last_order.order_id.split('-')[-1])
                new_number = f"{last_number + 1:04}"  # Format as a 4-digit number with leading zeros
            else:
                new_number = "0001"  # Start from 0001 if no previous order exists
            
            # Set the order_id with prefix and new incremental number
            self.order_id = f"{prefix}-{new_number}"
        
        super().save(*args, **kwargs)


    def amount_paid(self):
        return self.total - self.balance

    def confirm_order(self):
        self.status = 'pending'
        for item in self.line_items.all():
            item.status = 'pending'
            item.save()
        self.save()


    def get_pending_items(self):
        return self.line_items.filter(batch__isnull=True)

    def get_complete_items(self):
        return self.line_items.filter(status = 'completed')


    def receipt_url(self):
        return  reverse('print_receipt' , args=[self.id])


    def items_count(self):
        result=0
        for elm in self.items:

            result = result + elm.quantity 

        return result
    
    def update_payment_state(self):
        if self.balance == 0:
            self.payment_status = 'complete'
        elif self.balance < self.total:
            self.payment_status = 'partial'
        else: 
            self.payment_status = 'pending'

        self.save()

    def add_item(self, item):
        OrderLineItem.objects.create(
            item_type_id=item["item_type"],
            characteristic_id=item["charac"],
            service_id=item['service'],
            base_price=item["unit_price"],
            quantity=item["quantity"],
            order=self,
            description=item["description"],
            color = item["color"],
            brand = item["brand"],
            anormaly = item["anormalie"]
        )

    
    def update_item(self, item):
        id = item["id"]

        if id:
            line = OrderLineItem.objects.get(id = id)

            line.item_type_id  = item["item_type"]
            line.characteristic_id  = item["charac"]
            line.service_id  = item['service']
            line.base_price  = item["unit_price"]
            line.quantity  = item["quantity"]
            line.order  = self
            line.description  = item["description"]
            line.color = item["color"]
            line.brand = item["brand"]
            line.anormaly = item["anormalie"]

            line.save()

        else:
            OrderLineItem.objects.create(
                item_type_id=item["item_type"],
                characteristic_id=item["charac"],
                service_id=item['service'],
                base_price=item["unit_price"],
                quantity=item["quantity"],
                order=self,
                description=item["description"],
                color = item["color"],
                brand = item["brand"],
                anormaly = item["anormalie"]
            )
    
    def update_status(self):
        line_item_statuses = set(self.line_items.values_list('status', flat=True))
        #print(line_item_statuses)
        
        if all(status == 'delivered' for status in line_item_statuses):
            self.status = 'delivered'
        elif all(status == 'completed' for status in line_item_statuses):
            self.status = 'complete'
        elif 'production' in line_item_statuses and 'pending' in line_item_statuses:
            self.status = 'partial_production'
        elif 'production' in line_item_statuses:
            self.status = 'production'
        elif 'draft' in line_item_statuses:
            self.status = 'draft'
        else:
            self.status = 'pending'
        
        self.save()

    def update_balance(self):
        payments_total = sum(payment.amount for payment in self.payments.all())
        self.balance = self.total - payments_total
        if self.balance < 0:
            self.balance = 0
        self.save()


class OrderLineItem(models.Model):
    ORDER_LINE_STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'Pending'),
        ('production', 'In Production'),
        ('complete', 'Complete'),
        ('delivered', 'Delivered')
    ]

    ANORMALY_CHOICES = [
        ('Dechirure', 'Dechirure'),
        ('Tache', 'Tache'),
        ('Moisissure', 'Moisissure'),
        ('Teinte', 'Teinte'),
        ('Delaver', 'Delaver'),
        ('Trou' , "Trou"),
        ("Rouille" , " Rouille"),
        ("Boue" , "Boue"),
        ("Encre" , "Encre"),
        ("Aureole" , "Aureole"),
        ("Brullure" , "Brullure"),
        ("Effiloche" , "Effiloche"),
        ("Deteint" , "Deteint"),
        ("Decousu" , "Decousu"),
        ("Bouton Manquant" , "Bouton Manquant")

    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="line_items")
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(ItemCharacteristic, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    base_price = models.IntegerField()
    line_total = models.IntegerField(editable=False)
    batch = models.ForeignKey(Batch, related_name='items', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=50, choices=ORDER_LINE_STATUS_CHOICES, default='draft')
    color = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=255, null=True)
    anormaly = models.CharField(max_length=255, choices=ANORMALY_CHOICES, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.line_total = self.base_price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_status()




class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('mobile', 'Mobile Money'),
    ]

    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.IntegerField()
    session = models.ForeignKey('Core.SaleSession', on_delete=models.SET_NULL, null=True, blank=True)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update order balance whenever a payment is made
        self.order.update_balance()
        self.order.update_payment_state()
        if self.session:
            self.session.add_fund(Decimal(self.amount)) 

    def __str__(self):
        return f"Payment of {self.amount} for Order #{self.order.pk}"