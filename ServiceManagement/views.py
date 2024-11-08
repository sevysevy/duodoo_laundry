# views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ItemCategory, PriceList, Service , ItemType , ItemCharacteristic
from .forms import ItemCategoryForm, PriceListForm, ServiceForm , ItemTypeForm , ItemCharacteristicForm
from django.core.paginator import Paginator

def service_list(request):
    services = Service.objects.all()
    paginator = Paginator(services, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'service_list.html', {'services': page_obj})

def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service créé avec succès.")
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'service_form.html', {'form': form})

def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service mis à jour avec succès.")
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service_form.html', {'form': form})

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service supprimé avec succès.")
        return redirect('service_list')
    return render(request, 'service_confirm_delete.html', {'service': service})





# List all item types
def itemtype_list(request):
    item_types = ItemType.objects.all()
    paginator = Paginator(item_types, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'itemtype_list.html', {'item_types': page_obj})

# Create a new item type
def itemtype_create(request):
    if request.method == 'POST':
        form = ItemTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itemtype_list')
    else:
        form = ItemTypeForm()
    return render(request, 'itemtype_form.html', {'form': form})

# Update an item type
def itemtype_update(request, pk):
    item_type = get_object_or_404(ItemType, pk=pk)
    if request.method == 'POST':
        form = ItemTypeForm(request.POST, instance=item_type)
        if form.is_valid():
            form.save()
            return redirect('itemtype_list')
    else:
        form = ItemTypeForm(instance=item_type)
    return render(request, 'itemtype_form.html', {'form': form})

# Delete an item type
def itemtype_delete(request, pk):
    item_type = get_object_or_404(ItemType, pk=pk)
    if request.method == 'POST':
        item_type.delete()
        return redirect('itemtype_list')
    return render(request, 'itemtype_confirm_delete.html', {'item_type': item_type})



def itemcharacteristic_list(request):
    characteristics = ItemCharacteristic.objects.all()
    paginator = Paginator(characteristics, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'itemcharacteristic_list.html', {'characteristics': page_obj})

def itemcharacteristic_create(request):
    if request.method == 'POST':
        form = ItemCharacteristicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itemcharacteristic_list')
    else:
        form = ItemCharacteristicForm()
    return render(request, 'itemcharacteristic_form.html', {'form': form})

def itemcharacteristic_update(request, pk):
    characteristic = get_object_or_404(ItemCharacteristic, pk=pk)
    if request.method == 'POST':
        form = ItemCharacteristicForm(request.POST, instance=characteristic)
        if form.is_valid():
            form.save()
            return redirect('itemcharacteristic_list')
    else:
        form = ItemCharacteristicForm(instance=characteristic)
    return render(request, 'itemcharacteristic_form.html', {'form': form})


def itemcharacteristic_delete(request, pk):
    characteristic = get_object_or_404(ItemCharacteristic, pk=pk)
    if request.method == 'POST':
        characteristic.delete()
        return redirect('itemcharacteristic_list')
    return render(request, 'itemcharacteristic_confirm_delete.html', {'characteristic': characteristic})



def itemcategory_list(request):
    categories = ItemCategory.objects.all()

    paginator = Paginator(categories, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'itemcategory_list.html', {'categories': categories})

def itemcategory_create(request):
    if request.method == 'POST':
        form = ItemCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itemcategory_list')
    else:
        form = ItemCategoryForm()
    return render(request, 'itemcategory_form.html', {'form': form})

def itemcategory_update(request, pk):
    category = get_object_or_404(ItemCategory, pk=pk)
    if request.method == 'POST':
        form = ItemCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('itemcategory_list')
    else:
        form = ItemCategoryForm(instance=category)
    return render(request, 'itemcategory_form.html', {'form': form})

def itemcategory_delete(request, pk):
    category = get_object_or_404(ItemCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('itemcategory_list')
    return render(request, 'itemcategory_confirm_delete.html', {'category': category})


def itemcategory_detail(request, pk):
    category = get_object_or_404(ItemCategory, pk=pk)
    item_types = category.item_types.all()
    
    add_form = ItemTypeForm()  # Blank form for adding a new item type
    update_form = ItemTypeForm()  # Blank form, to be filled in dynamically

    if request.method == "POST":
        if 'item_type_id' in request.POST:
            item_type = get_object_or_404(ItemType, pk=request.POST['item_type_id'])
            update_form = ItemTypeForm(request.POST, instance=item_type)
            if update_form.is_valid():
                update_form.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "errors": update_form.errors}, status=400)
        else:
            add_form = ItemTypeForm(request.POST)
            if add_form.is_valid():
                new_item = add_form.save(commit=False)
                new_item.category = category
                new_item.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "errors": add_form.errors}, status=400)

    return render(request, 'itemcategory_detail.html', {
        'category': category,
        'item_types': item_types,
        'add_form': add_form,
        'update_form': update_form,
    })



def pricelist_list(request):
    pricelist = PriceList.objects.all()
    paginator = Paginator(pricelist, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pricelist_list.html', {
        'pricelist': page_obj
    })




# Delete a PriceList entry
def pricelist_delete(request, pk):
    pricelist_entry = get_object_or_404(PriceList, pk=pk)
    if request.method == 'POST':
        pricelist_entry.delete()
        messages.success(request, "Entrée de prix supprimée avec succès.")
        return redirect('pricelist_list')
    return render(request, 'pricelist_confirm_delete.html', {
        'pricelist_entry': pricelist_entry
    })

# AJAX view to get ItemTypes by selected Category
def get_item_types_by_category(request, category_id):
    item_types = ItemType.objects.filter(category_id=category_id)
    item_types_data = [{"id": item_type.id, "name": item_type.name} for item_type in item_types]
    return JsonResponse({"item_types": item_types_data})




def pricelist_create(request):
    if request.method == 'POST':
        form = PriceListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrée de prix créée avec succès.")
            return redirect('pricelist_list')
    else:
        form = PriceListForm()

    # Load data needed for the form selections
    services = Service.objects.all()
    categories = ItemCategory.objects.all()
    characteristics = ItemCharacteristic.objects.all()

    return render(request, 'pricelist_form.html', {
        'form': form,
        'services': services,
        'categories': categories,
        'characteristics': characteristics
    })

# Update an existing PriceList entry
def pricelist_update(request, pk):
    pricelist_entry = get_object_or_404(PriceList, pk=pk)
    if request.method == 'POST':
        form = PriceListForm(request.POST, instance=pricelist_entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrée de prix mise à jour avec succès.")
            return redirect('pricelist_list')
    else:
        form = PriceListForm(instance=pricelist_entry)

    services = Service.objects.all()
    categories = ItemCategory.objects.all()
    characteristics = ItemCharacteristic.objects.all()

    return render(request, 'pricelist_form.html', {
        'form': form,
        'services': services,
        'categories': categories,
        'characteristics': characteristics
    })