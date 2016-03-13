from django.shortcuts import render
from app.models import *
from .forms import CustomerForm
from django.shortcuts import redirect
from django.http import JsonResponse
import json

def index(request):
    customers = Customer.objects.all()
    context = {'customers':customers}
    return render(request, 'app/index.html', context)

def customer(request,c_id):
    customer=Customer.objects.get(id=c_id)
    whs = customer.warehouse_set.all()
    context = {'whs':whs,'customer':customer}
    return render(request, 'app/customer.html', context)

def warehouse(request,wh_id):
    #inventory for a Warehouse (Customer x's in City y)
    wh = Warehouse.objects.get(id=wh_id)
    customer = wh.customer
    city = wh.city
    wh_items = wh.warehouseinventory_set.all()
    items = []
    for whi in wh_items:
        part_list = []
        for j in ItemPs.objects.filter(item=whi.item):
            part_list.append(str(j))
        row=[whi.item.name,whi.amt,part_list]
        items.append(row)
    context = {'customer':customer,'city':city,'items':items}
    return render(request, 'app/warehouse.html', context)

def customer_new(request):
    if request.method == "POST":
        form = CustomerForm(request.CUSTOMER)
        if form.is_valid():
            post = form.save(commit=False)
            post.employee = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('customer',pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'app/customer_edit.html', {'form': form})

# Create your views here.
