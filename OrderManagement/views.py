import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render , redirect
from django.core.paginator import Paginator
# Create your views here.

from django.shortcuts import render
from django.db.models import Prefetch
from django.urls import reverse 
from Core.models import SaleSession
from ServiceManagement.models import ItemCategory, PriceList, Service
from UserManagement.models import Role, UserProfile
from .models import ItemType, ItemCharacteristic, Order
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import *
from .forms import *
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    categories = ItemCategory.objects.prefetch_related(
        Prefetch(
            'item_types',
            queryset=ItemType.objects.filter(
                price_entries__isnull=False  # Only include item types with PriceList entries
            ).distinct()
        )
    )
    characteristics = ItemCharacteristic.objects.all()
    agency = Agency.objects.last()

    anormalies =  OrderLineItem._meta.get_field('anormaly').choices
    
    today = timezone.now().date()
    session = SaleSession.objects.filter(
        status='open',
        start_time__date=today
    ).first()

    if request.method == "POST":
        print(request.POST)  # Check form data in the console for debugging
        count = request.POST.get("count")
        client_id = request.POST.get("client")
        confirm   = request.POST.get("confirm")
        payment  = request.POST.get("initial_payment")
        payment_method  = request.POST.get("payment_method")
        delivery_date    = request.POST.get("delivery_date")
        items = []
        order_total = 0  # Initialize total to zero

        # Loop through each item and calculate line totals
        for n in range(0, int(count)):
            unit_price = float(request.POST.get(f"items[{n}][unit_price]", 0))
            quantity = int(request.POST.get(f"items[{n}][quantity]", 0))
            line_total = unit_price * quantity  # Calculate line total
            description  = request.POST.get(f"items[{n}][description]")
            color  = request.POST.get(f"items[{n}][color]")
            brand  = request.POST.get(f"items[{n}][brand]")
            anormalie  = request.POST.get(f"items[{n}][anormalie]")
            
            items.append({
                "item_type": request.POST.get(f"items[{n}][item_type]"),
                "charac":  request.POST.get(f"items[{n}][characteristic]"),
                "service": request.POST.get(f"items[{n}][service]"),
                "unit_price": unit_price,
                "quantity": quantity,
                "line_total": line_total,
                "description": description,
                "color": color,
                "brand": brand,
                "anormalie": anormalie
            })

            # Add line total to the overall order total
            order_total += line_total

        if agency:
            # Create Order with calculated total
            if delivery_date:
                order = Order.objects.create(
                    client_id=client_id,
                    total=order_total,  # Set total with calculated value
                    status = 'draft',
                    delivery_date = delivery_date,
                    session = session,
                    agency = agency
                )
            else:
                order = Order.objects.create(
                    client_id=client_id,
                    total=order_total,  # Set total with calculated value
                    status = 'draft',
                    session = session,
                    agency = agency
                )

            order.update_balance()

            if payment != 0 and payment_method != '':

                payment = Payment.objects.create(order=order , amount = payment , payment_method = payment_method)
            
            # Add each item to the order
            for item in items:
                order.add_item(item)  # Assuming order.add_item handles creating OrderItem entries

            
            if confirm:
                order.confirm_order()

            receipt_url = reverse(order_receipt , args=[order.id])

            return JsonResponse({"result": "success", "order_total": order_total , "receipt":receipt_url})

    return render(request, 'order_form.html', {
        'categories': categories,
        'characteristics': characteristics,
        'anormalies':anormalies,
        'delivery_date': (today  + timedelta(days=2)).strftime('%d/%m/%Y')
    })

@login_required
def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        if order.status == 'draft':

            items = order.line_items.all()
            for item in items:
                item.delete()
            order.delete()
        return redirect('order_list')
    return render(request, 'order_confirm_delete.html', {'order': order})

@login_required
def order_update(request, pk):

    order = get_object_or_404(Order, id=pk)
    order_items = order.line_items.all()  
    for it in order_items:
        print(it.anormaly)

    categories = ItemCategory.objects.prefetch_related(
        Prefetch(
            'item_types',
            queryset=ItemType.objects.filter(
                price_entries__isnull=False  # Only include item types with PriceList entries
            ).distinct()
        )
    )
    characteristics = ItemCharacteristic.objects.all()
    services  = Service.objects.all()
    anormalies =  OrderLineItem._meta.get_field('anormaly').choices


    if request.method == "POST":
        print(request.POST)  # Check form data in the console for debugging
        count = request.POST.get("count")
        client_id = request.POST.get("client")
        order_id  = request.POST.get("order_id")
        confirm   = request.POST.get("confirm")

        items = []
        order_total = 0  # Initialize total to zero
        ids = []

        # Loop through each item and calculate line totals
        for n in range(0, int(count)):
            unit_price = float(request.POST.get(f"items[{n}][unit_price]", 0))
            quantity = int(request.POST.get(f"items[{n}][quantity]", 0))
            line_total = unit_price * quantity  # Calculate line total
            description  = request.POST.get(f"items[{n}][description]")
            item_type =  request.POST.get(f"items[{n}][item_type]")
            charac  =  request.POST.get(f"items[{n}][characteristic]")
            service = request.POST.get(f"items[{n}][service]")
            id = request.POST.get(f"items[{n}][id]" , None)
            ids.append(id)
            color  = request.POST.get(f"items[{n}][color]")
            brand  = request.POST.get(f"items[{n}][brand]")
            anormalie  = request.POST.get(f"items[{n}][anormalie]")

            items.append({
                "item_type": item_type,
                "charac":  charac,
                "service": service,
                "unit_price": unit_price,
                "quantity": quantity,
                "line_total": line_total,
                "description": description,
                "id":id,
                "color": color,
                "brand": brand,
                "anormalie": anormalie
            })

            # Add line total to the overall order total
            order_total += line_total


        try:
            # Create Order with calculated total
            order = Order.objects.get(id = order_id)
            order.client_id = client_id
            order.total = order_total
            
            order.save()

            print(order.line_items.all())
            for l_item in order.line_items.all():
                if str(l_item.id) not in ids:
                    l_item.delete()
            
            # Add each item to the order
            for item in items:
                order.update_item(item)  # Assuming order.add_item handles creating OrderItem entries


            if confirm:
                order.confirm_order()
           
        except:

            return JsonResponse({"result": "error", "message": "Cette commande est introuvable"})


        receipt_url = reverse(order_receipt , args=[order.id])

        return JsonResponse({"result": "success", "order_total": order_total , "receipt":receipt_url})


    return render(request, 'order_update.html', {
        'order': order,
        'order_items': order_items,
        'categories': categories,
        'characteristics': characteristics,
        'services': services,
        'anormalies':anormalies
    })


def get_customers(request):
    # Filter clients by role name_code 'customer'
    customer_role = Role.objects.get(name="Customer")
    customers = UserProfile.objects.filter(role=customer_role)
    
    # Format data as JSON
    data = [{"id": customer.id, "name": f"{customer.title} {customer.firstName} {customer.lastName} ( {customer.quartier} )"} for customer in customers]
    return JsonResponse(data, safe=False)

def get_item_types(request):
    # Fetch categories and item types in JSON format
    categories = ItemCategory.objects.prefetch_related(
        Prefetch(
            'item_types',
            queryset=ItemType.objects.filter(
                pricelist__isnull=False  # Ensures only item types with a PriceList entry are included
            ).distinct()  # Prevent duplicate item types if they appear in multiple PriceList entries
        )
    )
    data = {
        "categories": [
            {
                "id": category.id,
                "name": category.name,
                "item_types": [{"id": item_type.id, "name": item_type.name} for item_type in category.itemtype_set.all()]
            } for category in categories
        ]
    }
    return JsonResponse(data)


def add_client(request):
    if request.method == "POST":
        title = request.POST.get("title")
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        phone = request.POST.get("phone")
        ville = request.POST.get("ville")
        quartier = request.POST.get("quartier")

        role = Role.objects.get(name="Customer")
        # Save the new client
        new_client = UserProfile.objects.create(
            title=title,
            firstName=first_name,
            lastName=last_name,
            phone=phone,
            quartier = quartier,
            ville = ville,
            role = role
            # Add other fields if they exist in UserProfile model
        )



        return JsonResponse({"success": True})
    return JsonResponse({"success": False})



def get_price(request):
    item_type_id = request.GET.get('item_type_id')
    characteristic_id = request.GET.get('characteristic_id')
    service_id = request.GET.get('service_id')
    
    
    try:
        price_entry = PriceList.objects.get(
            service_id=service_id,
            item_type_id=item_type_id,
            item_characteristic_id=characteristic_id
        )
        price = price_entry.price
    except PriceList.DoesNotExist:
        price = None  # No matching price found

    return JsonResponse({'price': price})


def get_characteristics_for_item_type(request):
    item_type_id = request.GET.get('item_type_id')

    # Get the unique characteristics available for the selected item type in the PriceList
    characteristics = ItemCharacteristic.objects.filter(
        price_entries__item_type_id=item_type_id
    ).distinct()

    # Format the characteristics for JSON response
    data = [{"id": char.id, "name": char.name} for char in characteristics]
    return JsonResponse(data, safe=False)


def get_sevice_for_item_type(request):
    charac_id = request.GET.get('charac_id')

    # Get the unique characteristics available for the selected item type in the PriceList
    services = Service.objects.filter(
        price_entries__item_characteristic_id=charac_id
    ).distinct()

    # Format the characteristics for JSON response
    data = [{"id": char.id, "name": char.name} for char in services]
    return JsonResponse(data, safe=False)


def order_list(request):
    # Fetch all orders from the database, optionally filter or sort as needed
    orders = Order.objects.all().order_by('-created_at')  # Adjust ordering as needed
    status = request.GET.get('status')

    if status:
        orders = Order.objects.filter(status = status).order_by('-created_at')  # Adjust ordering as needed


    # Paginate the orders to limit the number displayed per page
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
    }
    return render(request, 'order_list.html', context)


@login_required
def order_detail(request, pk):
    # Fetch the order and related items
    order = get_object_or_404(Order, pk=pk)

    # Calculate totals if needed
    total_before_discount = sum(item.line_total for item in order.line_items.all())
    discount_amount = total_before_discount - order.ristourne  if order.ristourne else 0
    #total_after_discount = total_before_discount - discount_amount
    batches = Batch.objects.filter(items__order=order).distinct()

    payments = order.payments.all()

    context = {
        'order': order,
        'payments': payments,
        'batches': batches,
        'total_before_discount': total_before_discount,
        'total_after_discount': discount_amount,
    }
    return render(request, 'order_detail.html', context)



@login_required
def register_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    today = timezone.now().date()
    session = SaleSession.objects.filter(
        status='open',
        start_time__date=today
    ).first()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.session = session
            payment.save()  # This will automatically update the order balance
            return JsonResponse({"result": "success", "balance": order.balance})
        else:
            return JsonResponse({"result": "error", "errors": form.errors})

    else:
        form = PaymentForm()

    return render(request, 'register_payment.html', {'order': order, 'form': form})


def create_batch(request):
    agency = Agency.objects.last()
    if request.method == "POST":
        item_ids = request.POST.getlist('order_items[]')
        
        if not item_ids:
            return JsonResponse({"result": "error", "errors": "Pas de vetement selectionner"}, status=400)
        
        if not agency :
            return JsonResponse({"result": "error", "errors": "Veuillez configurer votre agence."}, status=403)
            

        new_batch = Batch.objects.create( agency = agency)

        new_batch.add_items_to_batch(item_ids)

        return JsonResponse({"result": "success", "batch_id": new_batch.batch_id})
    else:
        return JsonResponse({"result": "error", "errors": "Invalid request method"}, status=405)
    

def create_batch_multy(request):
    agency = Agency.objects.last()
    if request.method == "POST":
        print(request.POST)
        count = request.POST.get("count")

        if int(count) == 0:
            return JsonResponse({"result": "error", "errors": "Pas de vetement selectionner"}, status=400)
        
        if not agency :
            return JsonResponse({"result": "error", "errors": "Veuillez configurer votre agence."}, status=403)
        
        
        new_batch = Batch.objects.create(agency = agency)
        items = []

        # Loop through each item and calculate line totals
        for n in range(0, int(count)):
            item_id = request.POST.get(f"order_items[{n}][item_id]")
            print(item_id)
            items.append(item_id)
        
        
        print(items) 
        new_batch.add_items_to_batch(items)
           
        receipt_url = reverse(batch_receipt , args=[new_batch.id])
        return JsonResponse({"result": "success", "batch_id": new_batch.batch_id , 'receipt':receipt_url})
    else:
        return JsonResponse({"result": "error", "errors": "Invalid request method"}, status=405)
    


def batch_detail(request, batch_id):
    # Retrieve the specific batch by batch_id
    batch = get_object_or_404(Batch, batch_id=batch_id)
    
    # Get all items associated with this batch
    items = batch.items.all()

    return render(request, 'batch_detail.html', {
        'batch': batch,
        'items': items,
    })


@require_POST
def update_batch_status(request, batch_id):
    batch = get_object_or_404(Batch, batch_id=batch_id)
    status = request.POST.get('status')

    if status:
        batch.status = status
        batch.save()

        if status == 'completed':
            batch.complete_batch()
        return JsonResponse({"result": "success"})
    else:
        return JsonResponse({"result": "error", "errors": "Invalid status value"}, status=400)
    


def batch_list(request):
    # Retrieve all batches
    batches = Batch.objects.all().order_by('-created_at')  # Order by creation date, most recent first

    paginator = Paginator(batches, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    available_item = OrderLineItem.objects.filter(batch__isnull=True).order_by('-created_at')
    for it in available_item:
        print(f"{it.batch}--------{it.id}")

    return render(request, 'batch_list.html', {
        'batches': page_obj,
        'available_items': available_item
    })


@require_POST
def mark_items_as_delivered(request):
    item_ids = request.POST.getlist('order_item_ids[]')
    
    # Update the status of selected items to 'delivered'
    items = OrderLineItem.objects.filter(id__in=item_ids)
    orders_to_update = [item.order for item in items]  # Get unique orders for the updated items

    for order in orders_to_update:
        if order.balance != 0:
            return JsonResponse({"result":"error" , "errors":"Impossible de livrer des vetements la facture n'est pas completement paye"})

        order.update_status()

    items.update(status='delivered')
    

    return JsonResponse({"result": "success"})






def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', order_id=order.id)  # Redirect to order detail page after update
    else:
        form = UpdateOrderForm(instance=order)

    return render(request, 'update_order.html', {'form': form, 'order': order})


def order_receipt(request, pk):
    order = get_object_or_404(Order, id=pk)
    
   

    return render(request, 'order_receipt.html', { 'order': order})



def batch_receipt(request, pk):
    batch = get_object_or_404(Batch, id=pk)
    
    return render(request, 'batch_receipt.html', { 'batch': batch})