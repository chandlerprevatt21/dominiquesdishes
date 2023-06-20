from django.shortcuts import render
from orders.models import Order
from customers.models import Customer
from menus.models import Menu as General_Menu
from catering.models import Menu as Catering_Menu

def home(request):
    menus = General_Menu.objects.all()
    catering_menus = Catering_Menu.objects.all()
    orders = Order.objects.all()
    customers = Customer.objects.all()
    context = {
        'menus': menus,
        'catering_menus': catering_menus,
        'orders': orders,
        'customers': customers,
    }
    return render(request, 'dashboard_home.html', context)